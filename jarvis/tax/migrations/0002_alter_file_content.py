# Generated by Django 4.1.6 on 2023-06-20 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='content',
            field=models.FileField(upload_to='static/files/'),
        ),
    ]
