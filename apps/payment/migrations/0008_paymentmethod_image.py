# Generated by Django 4.2.6 on 2023-11-19 17:17

import apps.common.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_remove_paymentmethod_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='image',
            field=models.ImageField(null=True, upload_to='', validators=[apps.common.utils.validate_file_size]),
        ),
    ]
