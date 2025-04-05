# Generated by Django 4.1.6 on 2023-09-20 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0024_hollydaysreservation_renting_person_city_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hollydaysreservation',
            old_name='received_money',
            new_name='price',
        ),
        migrations.AddField(
            model_name='hollydaysreservation',
            name='received_bank',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
