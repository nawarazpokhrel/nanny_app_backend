# Generated by Django 4.2.6 on 2023-11-19 16:19

import apps.common.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_rename_paid_by_payment_to_be_paid_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('paypal', 'PayPal'), ('google_pay', 'Google Pay'), ('apple_pay', 'Apple Pay')], default='credit_card', max_length=20, unique=True)),
                ('image', models.ImageField(upload_to='payment_images/', validators=[apps.common.utils.validate_file_size])),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.paymentmethod'),
        ),
    ]
