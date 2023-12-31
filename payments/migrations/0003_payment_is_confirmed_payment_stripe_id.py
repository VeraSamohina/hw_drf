# Generated by Django 4.2.6 on 2023-11-11 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name='Подтвержден'),
        ),
        migrations.AddField(
            model_name='payment',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='id платежного намерения'),
        ),
    ]
