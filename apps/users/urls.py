from django.urls import path
from apps.users import views

urlpatterns = [
    path(
        'register',
        views.CreateUserView.as_view(),
        name='register-user'

    ),
    path(
        'list',
        views.ListUserView.as_view(),
        name='list-user'

    ),

    path(
        '<int:user_id>/user-profile',
        views.CreateUserProfileView.as_view(),
        name='personal-info-view'

    ),
    path(
        '<int:user_id>/detail',
        views.UserDetailView.as_view(),
        name='user-detail'

    ),

]
