# Generated by Django 4.2.6 on 2023-11-05 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0007_rename_childcareneed_experience'),
        ('users', '0013_rename_expectation_userprofile_experience_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='experience',
            field=models.ManyToManyField(to='skills.experience'),
        ),
    ]
