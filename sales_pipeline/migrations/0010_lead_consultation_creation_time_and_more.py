# Generated by Django 4.2.9 on 2025-01-03 08:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sales_pipeline', '0009_consultation'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='consultation_creation_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='follow_up_creation_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]