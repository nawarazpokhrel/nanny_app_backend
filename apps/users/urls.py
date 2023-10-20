from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users import views
from apps.users.views import CustomTokenObtainPairView, AddToFavoritesView

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

    path(
        'list/nannies',
        views.ListUserPersonalDetailView.as_view(),
        name='user-personal-detail-list'

    ),
    path(
        '<int:user_id>/nannies-detail',
        views.UserPersonalDetailView.as_view(),
        name='user-personal-detail'

    ),
    path(
        'auth/login/',
        CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path('auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'
         ),
    path('add-to-favourites',
         AddToFavoritesView.as_view(),
         name='add-to-favourites'
         ),
    path('list-favourites',
         views.ListFavoritesView.as_view(),
         name='list-favourites'
         ),
    # path('nanny-search',
    #      views.NannySearchView.as_view(),
    #      name='search-nanny'
    #      ),
]
