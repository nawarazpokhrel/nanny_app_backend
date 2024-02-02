# Generated by Django 4.2.6 on 2023-11-04 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_user_favorites'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='expectation',
            new_name='experience',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='experience_years',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
