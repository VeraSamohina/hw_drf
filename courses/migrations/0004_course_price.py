# Generated by Django 4.2.6 on 2023-11-10 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='цена'),
        ),
    ]
