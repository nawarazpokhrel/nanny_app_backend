from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.booking.permissions import IsParent
from apps.common.choices import UserRole
from apps.users import serializers, usecases
from apps.users.filters import filter_nannies
from apps.users.models import UserProfile
from apps.users.serializers import CreateProfileSerializer, UserPersonalDetailSerializer, MyTokenObtainPairSerializer, \
    AddToFavoritesSerializer, ListUserSerializer, SearchCriteriaSerializer

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


class CreateUserProfileView(generics.CreateAPIView):
    serializer_class = CreateProfileSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'user does not exist for following id.'}
            )

    def perform_create(self, serializer):
        return usecases.CreateUserProfileUseCase(
            serializer=serializer,
            user=self.get_object(),
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

    # def get_object(self):
    #     user_id = self.kwargs.get('user_id')
    #     try:
    #         user = User.objects.get(pk=user_id)
    #         return user
    #     except User.DoesNotExist:
    #         raise ValidationError(
    #             {'error': 'user does not exist for following id.'}
    #         )

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
                {'error': 'user does not exist for following id.'}
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class AddToFavoritesView(generics.CreateAPIView):
    serializer_class = AddToFavoritesSerializer

    permission_classes = [IsParent]

    def perform_create(self, serializer):
        try:
            user = User.objects.get(pk=serializer.validated_data.get('id'))
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'user does not exist for following id.'}
            )
        if hasattr(self.request.user, 'userprofile'):
            if user in self.request.user.userprofile.favorites.all():
                raise ValidationError({'error': 'This user is already in your favorites.'})
            self.request.user.userprofile.favorites.add(user)

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
    serializer_class = ListUserSerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        return self.request.user.userprofile.favorites.all()


class NannySearchView(generics.CreateAPIView):
    serializer_class = serializers.SearchCriteriaSerializer
    queryset = ''

    # This serializer should represent the nanny data structure you want to return

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filtered_nannies = filter_nannies(serializer.validated_data)

        # Serialize the filtered nannies
        nanny_serializer = serializers.UserPersonalProfileSerializer(filtered_nannies, many=True)

        return Response(nanny_serializer.data, status=status.HTTP_200_OK)
