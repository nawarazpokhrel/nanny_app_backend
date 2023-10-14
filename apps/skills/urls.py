from django.urls import path
from apps.skills.views import ListAvailiabilityView, ListSkillView, LisTimeSlotView, ListDaysView


urlpatterns = [
    path('availiability', ListAvailiabilityView.as_view(), name = 'availiability'),
    path('skills', ListSkillView.as_view(), name = 'list_of_skills'),
    path('time', LisTimeSlotView.as_view(), name = 'time'),
    path('days', ListDaysView.as_view(), name = 'days'),
]