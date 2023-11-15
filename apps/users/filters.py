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
        commitment_type_list = list(data['commitment_type'])
        queryset = queryset.filter(commitment_type__id__in=commitment_type_list).distinct()

        # Filter by experiences_required
    if data.get('experiences_required'):
        experiences_required_list = list(data['experiences_required'])
        queryset = queryset.filter(experience__id__in=experiences_required_list).distinct()
    if data.get('min_age') and data.get('max_age'):
        # Filter by age
        max_birth_date_for_min_age = (timezone.now() - timedelta(days=data['min_age'] * 365.25)).date()

        # Min date of birth for age < 25
        min_birth_date_for_max_age = (timezone.now() - timedelta(days=data['max_age'] * 365.25)).date() + timedelta(
            days=1)

        # Apply filters
        queryset = queryset.filter(date_of_birth__gte=min_birth_date_for_max_age,
                                   date_of_birth__lt=max_birth_date_for_min_age)

    if data.get('min_experience') and data.get('max_experience'):
        # Filter by age

        queryset = queryset.filter(experience__gte=data.get('min_experience'),
                                   experience__lt=data.get('max_experience'))

    # Filter by city
    if data.get('city'):
        queryset = queryset.filter(
            city__icontains=data['city'])

    if data.get('language'):
        queryset = queryset.filter(
            language__icontains=data['language'])

    # Filter by skills
    if data.get('skills'):
        skills_list = list(data['skills'])
        q_skills = Q()
        for skill in skills_list:
            q_skills |= Q(skills__id=skill)
        queryset = queryset.filter(q_skills)

    if data.get('has_work_permit'):
        queryset = queryset.filter(
            has_work_permit=data['has_work_permit'])
        print(queryset)
    if data.get('has_first_aid_training'):
        queryset = queryset.filter(
            has_first_aid_training=data['has_first_aid_training'])
    if data.get('has_cpr_training'):
        queryset = queryset.filter(
            has_cpr_training=data['has_cpr_training'])
    if data.get('has_nanny_training'):
        queryset = queryset.filter(
            has_nanny_training=data['has_nanny_training'])

    return queryset
