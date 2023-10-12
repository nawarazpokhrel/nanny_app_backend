from django.db import models


class UserRole(models.TextChoices):
    NANNY = 'N', 'Nanny'
    PARENT = 'P', 'Parent'


COUNTRY_CHOICES = (
    ('CA','Canada'),
    ('CN', 'China'),
    ('IN', 'India'),
    ('US', 'United States'),
    ('ID', 'Indonesia'),
    ('PK', 'Pakistan'),
    ('BR', 'Brazil'),
    ('NG', 'Nigeria'),
    ('BD', 'Bangladesh'),
    ('RU', 'Russia'),
    ('MX', 'Mexico'),
    ('JP', 'Japan'),
    ('PH', 'Philippines'),
    ('ET', 'Ethiopia'),
    ('EG', 'Egypt'),
    ('VN', 'Vietnam'),
    ('CD', 'DR Congo'),
    ('TR', 'Turkey'),
    ('IR', 'Iran'),
    ('DE', 'Germany'),
    ('FR', 'France'),
    ('GB', 'United Kingdom'),
    ('TH', 'Thailand'),
    ('ZA', 'South Africa'),
    ('IT', 'Italy'),
    ('MM', 'Myanmar'),
    ('KR', 'South Korea'),
    ('CO', 'Colombia'),
    ('ES', 'Spain'),
    ('UA', 'Ukraine'),
    ('AR', 'Argentina')
)
