# Generated by Django 4.2.9 on 2024-12-30 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_pipeline', '0007_lead_follow_up_lead_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='follow_up_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
