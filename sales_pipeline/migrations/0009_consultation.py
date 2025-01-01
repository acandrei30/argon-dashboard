# Generated by Django 4.2.9 on 2024-12-31 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales_pipeline', '0008_lead_follow_up_date_lead_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alertness', models.CharField(max_length=50)),
                ('lives_alone', models.CharField(max_length=10)),
                ('house_suitable', models.CharField(max_length=10)),
                ('speech_impairment', models.CharField(max_length=20)),
                ('sight_impairment', models.CharField(max_length=20)),
                ('hearing_impairment', models.CharField(max_length=20)),
                ('locomotive_impairment', models.CharField(max_length=20)),
                ('lifting_required', models.CharField(max_length=10)),
                ('personal_help', models.CharField(max_length=10)),
                ('allergies', models.TextField(blank=True, null=True)),
                ('recent_hospitalization', models.CharField(max_length=10)),
                ('hospitalization_reason', models.TextField(blank=True, null=True)),
                ('lead', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='consultation', to='sales_pipeline.lead')),
            ],
        ),
    ]