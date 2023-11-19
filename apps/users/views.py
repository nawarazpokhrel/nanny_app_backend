import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.booking.models import Review
from apps.booking.permissions import IsParent, IsNanny
from apps.skills.models import TimeSlot
from apps.users import serializers, usecases
from apps.users.filters import filter_nannies, UserFilterSet, FavouriteUserFilterSet
from apps.users.models import UserAvailability
from apps.users.serializers import CreateProfileSerializer, UserPersonalDetailSerializer, MyTokenObtainPairSerializer, \
    AddToFavoritesSerializer, ChangePhoneNumberSerializer, ChangeImageSerializer, UserAvailabilitySerializer

User = get_user_model()


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer

    def perform_create(self, serializer):
        return usecases.CreateUserUseCase(serializer=serializer).execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {
            'data': serializer.data,
            'message': 'User created successfully',
            'status_code': status.HTTP_201_CREATED
        }
        return Response(data)


class ListUserView(generics.ListAPIView):
    serializer_class = serializers.ListUserSerializer

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['class'] = 'USER'
        return context


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.ListUserSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'user does not exist for following id.'}
            )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['class'] = 'USER'
        return context


class CreateUserProfileView(generics.CreateAPIView):
    serializer_class = CreateProfileSerializer
    permission_classes = [IsNanny, ]

    # parser_classes = (parsers.MultiPartParser,)

    def perform_create(self, serializer):
        return usecases.CreateUserProfileUseCase(
            serializer=serializer,
            user=self.request.user,
        ).execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {
            "message": "User profile created successfully",
            "status": status.HTTP_201_CREATED
        }
        return Response(data)


class ListUserPersonalDetailView(generics.ListAPIView):
    serializer_class = UserPersonalDetailSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilterSet
    permission_classes = [IsParent, ]

    def get_queryset(self):
        return User.objects.filter(role='N')


class UserPersonalDetailView(generics.RetrieveAPIView):
    serializer_class = UserPersonalDetailSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id, role='N')
            return user
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'Nanny user does not exist for following id.'}
            )

    def get_serializer_context(self):
        user = self.get_object()
        reviews = Review.objects.filter(booking__nanny=user)
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user_id'] = self.kwargs.get('user_id')
        context['requesting_user'] = self.request.user

        context['reviews'] = reviews
        return context


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class AddToFavoritesView(generics.CreateAPIView):
    serializer_class = AddToFavoritesSerializer

    permission_classes = [IsParent]

    def perform_create(self, serializer):
        if self.request.user == serializer.validated_data.get('id'):
            raise ValidationError(
                {'error': 'You cannot add favorites yourself!'}
            )

        try:
            user = User.objects.get(pk=serializer.validated_data.get('id'))
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'user does not exist for following id.'}
            )
        if user.role == 'P':
            raise ValidationError(
                {'error': 'You can only add users with the Nanny role as favorites.'}
            )

        if user in self.request.user.favorites.all():
            raise ValidationError({'error': 'This user is already in your favorites.'})
        self.request.user.favorites.add(user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {
            "message": "Favorite added successfully",
            "status": status.HTTP_201_CREATED
        }
        return Response(data)


class ListFavoritesView(generics.ListAPIView):
    serializer_class = serializers.UserPersonalProfileViaUserSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = FavouriteUserFilterSet
    permission_classes = [IsParent]

    def get_queryset(self):
        queryset = self.request.user.favorites.filter(role='N').all().order_by('-id')
        full_name_search = self.request.query_params.get('fullname', None)
        if full_name_search:
            queryset = queryset.filter(fullname__icontains=full_name_search)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['class'] = 'USER'
        return context


class NannySearchView(generics.CreateAPIView):
    serializer_class = serializers.SearchCriteriaSerializer
    queryset = ''
    permission_classes = [IsParent]

    # This serializer should represent the nanny data structure you want to return

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filtered_nannies = filter_nannies(serializer.validated_data)

        # Serialize the filtered nannies
        nanny_data = []
        for nanny in filtered_nannies:
            nanny_info = serializers.UserPersonalProfileSerializer(nanny, context=
            {'request': self.request,
             'class': "Search"
             }
                                                                   ).data
            if User.objects.get(pk=nanny_info.get('user_detail').get('id')) in self.request.user.favorites.all():
                nanny_info['has_been_favorite'] = True
            else:
                nanny_info['has_been_favorite'] = False

            nanny_data.append(nanny_info)
        return Response(nanny_data, status=status.HTTP_200_OK)


class RemoveFavoritesView(generics.CreateAPIView):
    serializer_class = AddToFavoritesSerializer

    permission_classes = [IsParent]

    def perform_create(self, serializer):
        if self.request.user.id == serializer.validated_data.get('id'):
            raise ValidationError(
                {'error': 'You cannot add or remove favorites by yourself!'}
            )

        try:
            user = User.objects.get(pk=serializer.validated_data.get('id'))
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'user does not exist for following id.'}
            )
        if user.role == 'P':
            raise ValidationError(
                {'error': 'You can only remove users with the Nanny role as favorites.'}
            )

        if user not in self.request.user.favorites.all():
            raise ValidationError({'error': 'This user is already unfavoured.'})
        self.request.user.favorites.remove(user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {
            "message": "Favorite removed successfully",
            "status": status.HTTP_201_CREATED
        }
        return Response(data)


class ChangePhoneNumberView(generics.CreateAPIView):
    queryset = ''
    serializer_class = ChangePhoneNumberSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        old_phone_number = serializer.validated_data.get('old_phone_number', None)
        new_phone_number = serializer.validated_data.get('new_phone_number', None)
        user = User.objects.filter(phone_number=old_phone_number).first()
        if not user:
            raise ValidationError({'error': 'User does not exist for old phone number.'})
        else:
            self.request.user.phone_number = new_phone_number
            self.request.user.save()


class ChangeProfileIMageView(generics.CreateAPIView):
    queryset = ''
    serializer_class = ChangeImageSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        image = serializer.validated_data.get('avatar', None)
        binary_data = base64.b64decode(image)
        file_content = ContentFile(binary_data)
        self.request.user.avatar.save(f'{self.request.user.fullname}_profile.jpg',
                                      file_content,
                                      )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response("Phone Number updated successfully", status=status.HTTP_200_OK, headers=headers)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response("Image saved successfully", status=status.HTTP_200_OK, headers=headers)


class ChangeAvailabilityView(generics.CreateAPIView):
    serializer_class = UserAvailabilitySerializer
    permission_classes = [IsNanny]

    def perform_create(self, serializer):
        day = serializer.validated_data.get('day', None)
        time_slots = serializer.validated_data.get('timeslots', None)
        seen_slugs = set()
        duplicate_slugs = set()

        for timeslot in time_slots:
            slug = timeslot["slug"]
            if slug in seen_slugs:
                duplicate_slugs.add(slug)
            else:
                seen_slugs.add(slug)
        if duplicate_slugs:
            raise ValidationError(
                {'error': 'Error same time slot not permitted.'}
            )
        userprofile = self.request.user.userprofile
        user_availabilities = UserAvailability.objects.filter(
            day=day,
            user_profile=userprofile
        ).first()
        if user_availabilities:
            for time_slot_data in time_slots:
                time_slot_name = time_slot_data.get('slug')
                time_slot = TimeSlot.objects.filter(slug=time_slot_name).first()
                if time_slot:
                    user_availabilities.timeslots.add(time_slot)
                else:
                    raise ValidationError({
                        'error': 'no timeslot found for following slug'
                    })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response("Time slot updated successfully", status=status.HTTP_201_CREATED, headers=headers)
