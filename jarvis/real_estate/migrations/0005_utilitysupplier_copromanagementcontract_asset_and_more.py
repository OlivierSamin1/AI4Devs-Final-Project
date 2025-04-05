# Generated by Django 4.1.6 on 2023-07-06 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('real_estate', '0004_alter_tenant_rental_ending_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='UtilitySupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('personal_email_used', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, help_text='ex: 682882017', max_length=12, null=True)),
                ('comments', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name_plural': 'Utility suppliers',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='copromanagementcontract',
            name='asset',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='copro_contract_tenant', to='real_estate.asset'),
        ),
        migrations.AddField(
            model_name='rentingmanagementcontract',
            name='asset',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='renting_contract_asset', to='real_estate.asset'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='copro_contract',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asset_copro_contract', to='real_estate.copromanagementcontract'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='renting_contract',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asset_renting_contract', to='real_estate.rentingmanagementcontract'),
        ),
        migrations.AlterField(
            model_name='copromanagementcontract',
            name='company',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='copro_contract_company', to='real_estate.copromanagementcompany'),
        ),
        migrations.CreateModel(
            name='UtilityContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal_email_used', models.EmailField(blank=True, max_length=254, null=True)),
                ('service', models.CharField(choices=[('waste management', 'waste management'), ('Electricity', 'Electricity'), ('Water', 'Water'), ('Internet', 'Internet'), ('Other', 'Other')], max_length=50, null=True)),
                ('contract_number', models.CharField(blank=True, max_length=50, null=True)),
                ('starting_date', models.DateField(blank=True, null=True)),
                ('ending_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(blank=True, null=True)),
                ('comments', models.CharField(blank=True, max_length=500, null=True)),
                ('asset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='utility_tenant', to='real_estate.asset')),
                ('supplier', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='utility_supplier', to='real_estate.utilitysupplier')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='utility', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Utility Contracts',
                'ordering': ['service', 'asset', 'user', 'is_active'],
            },
        ),
        migrations.CreateModel(
            name='FileUtility',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='real_estate.file')),
                ('access_to_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='RE_utility_files', to='real_estate.utilitycontract')),
            ],
            bases=('real_estate.file',),
        ),
    ]
