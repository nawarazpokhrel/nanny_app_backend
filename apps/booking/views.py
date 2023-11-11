from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError

from apps.booking import serializers
from apps.booking.filters import BookingFilter
from apps.booking.models import BookingDate, Booking, Review
from apps.booking.permissions import IsNanny, IsParent
from apps.booking.serializers import ListBookingSerializer, AcceptBookingSerializer
from apps.skills.models import TimeSlot, Availability
from apps.users.serializers import ListReviewSerializer

User = get_user_model()


# Create your views here.

class CreateBookingView(generics.CreateAPIView):
    serializer_class = serializers.CreateBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            if user.role != 'N':
                raise ValidationError(
                    {'error': 'user profile  need to be  Nanny to make booking.'}
                )
            else:
                return user
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'user does not exist for following id.'}
            )

    def perform_create(self, serializer):
        commitment_type = serializer.validated_data.pop('commitment')
        parent = self.request.user

        if parent.role != 'P':
            raise ValidationError(
                {'error': 'user profile  need to be  parent.'}
            )

        care_needs = serializer.validated_data.pop('care_needs')
        expectations = serializer.validated_data.pop('expectations')
        availabilities = serializer.validated_data.pop('availability')

        # check if booking exist and booking is in pending state

        booking = Booking.objects.filter(
            parent=parent,
            nanny=self.get_object(),
            status='pending'
        ).exists()

        if booking:
            raise ValidationError({
                'error': 'Cannot make next booking until your request is accepted by this nanny.'
            }
            )
        else:
            booking = Booking(
                parent=parent,
                nanny=self.get_object(),
                additional_message=serializer.validated_data.pop('additional_message'),
                status='pending',
                commitment=commitment_type,
            )
            booking.save()

        booking.expectations.add(*expectations)
        booking.care_needs.add(*care_needs)
        booking.save()
        for availability in availabilities:
            # days = availability.get('day')
            extracted_date = availability.get('date')
            time_slots = availability.get('time_slots')
            booking_date, created = BookingDate.objects.get_or_create(
                booking=booking,
                date=extracted_date,
            )

            for time_slot_data in time_slots:
                time_slot_name = time_slot_data.get('slug')
                time_slot, created = TimeSlot.objects.get_or_create(slugF=time_slot_name)
                booking_date.time_slots.add(time_slot)
            booking_date.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {
            "message": "Booking request created successfully",
            "status": status.HTTP_201_CREATED
        }
        return Response(data)


#
# {
#    "parent":2,
#    "care_needs":[
#       2
#    ],
#    "commitment":1,
#    "expectations":[
#       3,
#       4,
#       5
#    ],
#    "additional_message":"ok",
#    "availability":[
#       {
#          "day":{
#             "date":"2023-10-15"
#          },
#          "time_slots":[
#             {
#                "name":"MOR"
#             }
#          ]
#       }
#    ]
# }
#
class ListBookingView(ListAPIView):
    permission_classes = [IsNanny]
    serializer_class = ListBookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(nanny=self.request.user)


class AcceptBookingView(generics.CreateAPIView):
    permission_classes = [IsNanny]
    serializer_class = AcceptBookingSerializer

    def get_object(self):
        booking_id = self.kwargs.get('booking_id')
        try:
            booking = Booking.objects.get(pk=booking_id)
            return booking
        except Booking.DoesNotExist:
            raise ValidationError(
                {'error': 'Booking does not exist for following id.'}
            )

    def perform_create(self, serializer):
        booking = self.get_object()
        booking.status = serializer.validated_data.get('status')
        booking.save()

        # send notification


class ListAcceptedBookingView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ListBookingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookingFilter

    def get_queryset(self):
        if self.request.user.role == 'P':
            return Booking.objects.filter(status__in=['accepted', 'rejected', 'pending'], parent=self.request.user,
                                          parent__role='P')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = self.get_serializer(queryset, many=True).data
        if serialized_data:
            for item in serialized_data:
                user_id = item.get('nanny').get('user_detail').get('id')
                item['has_been_favorite'] = User.objects.get(pk=user_id) in self.request.user.favorites.all()

        return Response(serialized_data, status=status.HTTP_200_OK)


class AddReviewView(generics.CreateAPIView):
    permission_classes = [IsParent]
    serializer_class = serializers.ReviewSerializer

    def get_object(self):
        booking_id = self.kwargs.get('booking_id')
        try:
            booking = Booking.objects.get(pk=booking_id)
            return booking
        except Booking.DoesNotExist:
            raise ValidationError(
                {'error': 'Booking does not exist for following id.'}
            )

    def perform_create(self, serializer):
        booking = self.get_object()

        if Booking.objects.filter(pk=booking.id, status='accepted').exists():
            data = serializer.validated_data

            try:
                review = Review(user=self.request.user, booking=booking, **data)
                review.save()
            except IntegrityError:
                raise ValidationError({
                    'error': "review for this booking already exist"
                })
        else:
            raise ValidationError({
                'error': "No booking available for   review "
            })


class ListMyReviewView(ListAPIView):
    permission_classes = [IsParent, ]
    serializer_class = ListReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context =super().get_serializer_context()
        context['request'] = self.request
        context['class'] = "MyReview"
        return context
