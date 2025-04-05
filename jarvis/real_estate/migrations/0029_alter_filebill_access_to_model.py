# Generated by Django 4.1.6 on 2024-05-11 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0028_alter_filebill_access_to_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filebill',
            name='access_to_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='RE_bill_files', to='real_estate.bill'),
        ),
    ]
