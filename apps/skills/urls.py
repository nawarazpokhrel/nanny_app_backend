from django.urls import path
from apps.skills.views import ListAvailiabilityView, ListSkillView, LisTimeSlotView, ListDaysView, ListExpectationView, \
    CityListView, ListExperienceView, LanguageListView

urlpatterns = [
    path('availiability',
         ListAvailiabilityView.as_view(),
         name='availability'
         ),
    path(
        'list',
        ListSkillView.as_view(),
        name='list_of_skills'
    ),
    path(
        'time',
        LisTimeSlotView.as_view(),
        name='time'
    ),
    path(
        'days',
        ListDaysView.as_view(),
        name='days'
    ),
    path(
        'expectation-list',
        ListExpectationView.as_view(),
        name='days'
    ),
    path(
        'experience-list',
        ListExperienceView.as_view(),
        name='experience'
    ),
    path('cities/list', CityListView.as_view(), name='city-list'),
    path('languages/', LanguageListView.as_view(), name='language-list'),

]
