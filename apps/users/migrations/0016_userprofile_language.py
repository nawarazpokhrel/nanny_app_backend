# Generated by Django 4.2.6 on 2023-11-10 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_userprofile_city_alter_userprofile_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('de', 'German'), ('zh', 'Chinese')], max_length=10, null=True),
        ),
    ]