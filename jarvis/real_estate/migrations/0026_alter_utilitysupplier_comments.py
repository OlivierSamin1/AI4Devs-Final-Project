# Generated by Django 4.1.6 on 2023-09-21 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0025_rename_received_money_hollydaysreservation_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilitysupplier',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
