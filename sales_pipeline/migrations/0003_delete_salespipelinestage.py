# Generated by Django 4.2.9 on 2024-12-27 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales_pipeline', '0002_salespipelinestage_leadnotes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SalesPipelineStage',
        ),
    ]
