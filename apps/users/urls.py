from django.urls import path
from apps.users import views

urlpatterns = [
    path(
        'register',
        views.CreateUserView.as_view(),
        name='register-user'

    )
]