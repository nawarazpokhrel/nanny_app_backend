# Generated by Django 4.2.6 on 2023-11-16 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_payment_paid_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='paid_by',
            new_name='to_be_paid_by',
        ),
    ]
