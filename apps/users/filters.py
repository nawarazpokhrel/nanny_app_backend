from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

from apps.common.choices import UserRole
from apps.users.models import UserProfile

User = get_user_model()


def filter_nannies(data):
    # Start with all users with the nanny role
    queryset = UserProfile.objects.filter(user__role=UserRole.NANNY)

    # Filter by commitment type
    if data.get('commitment_type'):
        queryset = queryset.filter(commitment_type__availability__in=data['commitment_type']).distinct()
    if data.get('min_age') and data.get('max_age'):
        # Filter by age
        max_birth_date_for_min_age = (timezone.now() - timedelta(days=data['min_age'] * 365.25)).date()

        # Min date of birth for age < 25
        min_birth_date_for_max_age = (timezone.now() - timedelta(days=data['max_age'] * 365.25)).date() + timedelta(
            days=1)

        # Apply filters
        queryset = queryset.filter(date_of_birth__gte=min_birth_date_for_max_age,
                                   date_of_birth__lt=max_birth_date_for_min_age)

    # Filter by city
    if data.get('city'):
        queryset = queryset.filter(
            address__icontains=data['city'])

    # Filter by skills
    if data.get('skills'):
        q_skills = Q()
        for skill in data['skills']:
            q_skills |= Q(skills__skills=skill)
        queryset = queryset.filter(q_skills)

    return queryset
