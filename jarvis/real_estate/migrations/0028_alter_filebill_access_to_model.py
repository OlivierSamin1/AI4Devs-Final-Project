# Generated by Django 4.1.6 on 2024-05-11 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0027_alter_bill_options_alter_bill_asset_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filebill',
            name='access_to_model',
            field=models.ForeignKey(blank=True, default='bill', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='RE_bill_files', to='real_estate.bill'),
        ),
    ]
