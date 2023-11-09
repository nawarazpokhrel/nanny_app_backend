from django.core.management.base import BaseCommand

from apps.common.choices import (
    UserRole, COMMIT_CHOICES, SKILL_CHOICES, TIME_CHOICES, DAY_CHOICES,
    ExpectationTypeChoices, ChildCareNeedChoices
)
from apps.skills.models import Availability, Skills, TimeSlot, Days, Expectation, Experience


class Command(BaseCommand):
    help = 'Populate the database with initial choice data'

    def handle(self, *args, **kwargs):
        self.populate_availabilities()
        self.populate_skills()
        self.populate_time_slots()
        self.populate_days()
        self.populate_expectations()
        self.populate_experience()

    def populate_availabilities(self):
        for choice in COMMIT_CHOICES:
            obj, created = Availability.objects.get_or_create(availability=choice[0])
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Availability "{choice[1]}"'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Availability "{choice[1]}" already exists'))

    def populate_skills(self):
        for choice in SKILL_CHOICES:
            obj, created = Skills.objects.get_or_create(skills=choice[0])
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created skills "{choice[1]}"'))
            else:
                self.stdout.write(self.style.SUCCESS(f'skills "{choice[1]}" already exists'))

    def populate_time_slots(self):
        for choice in TIME_CHOICES:
            obj, created = TimeSlot.objects.get_or_create(name=choice[0])
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created time "{choice[1]}"'))
            else:
                self.stdout.write(self.style.SUCCESS(f'time "{choice[1]}" already exists'))

    def populate_days(self):
        for choice in DAY_CHOICES:
            obj, created = Days.objects.get_or_create(day_name=choice[0])
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created days "{choice[1]}"'))
            else:
                self.stdout.write(self.style.SUCCESS(f'days "{choice[1]}" already exists'))

    def populate_expectations(self):
        for choice in ExpectationTypeChoices.choices:
            obj, created = Expectation.objects.get_or_create(type=choice[0])
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created expectation "{choice[1]}"'))
            else:
                self.stdout.write(self.style.SUCCESS(f'expectation "{choice[1]}" already exists'))

    def populate_experience(self):
        for choice in ChildCareNeedChoices.choices:
            obj, created = Experience.objects.get_or_create(type=choice[0])
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created expectation "{choice[1]}"'))
            else:
                self.stdout.write(self.style.SUCCESS(f'expectation "{choice[1]}" already exists'))
