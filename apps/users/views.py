from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users import serializers, usecases
from apps.users.serializers import CreateProfileSerializer, UserPersonalDetailSerializer, MyTokenObtainPairSerializer

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

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'user does not exist for following id.'}
            )

    def get_queryset(self):
        return User.objects.filter(pk=self.get_object().id)


class UserPersonalDetailView(generics.RetrieveAPIView):
    serializer_class = UserPersonalDetailSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'user does not exist for following id.'}
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
