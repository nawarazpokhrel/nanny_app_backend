from django.urls import path

from apps.notification.views import NotificationListView

urlpatterns = [
    path(
        'list',
        NotificationListView.as_view(),
        name='notification-list'
    )
]
