# Generated by Django 4.1.6 on 2023-08-26 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0023_bill_is_location_commission_bill'),
    ]

    operations = [
        migrations.AddField(
            model_name='hollydaysreservation',
            name='renting_person_city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='hollydaysreservation',
            name='renting_person_country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='hollydaysreservation',
            name='renting_person_direction',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='hollydaysreservation',
            name='renting_person_dni',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='hollydaysreservation',
            name='renting_person_full_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hollydaysreservation',
            name='renting_person_postcode',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='hollydaysreservation',
            name='renting_person_region',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
