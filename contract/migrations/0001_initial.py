# Generated by Django 3.2 on 2021-06-07 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('provider', '0002_alter_provider_image'),
        ('status', '0001_initial'),
        ('service_type', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('object', models.TextField(verbose_name='Fantasy Name')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Slug')),
                ('dt_start', models.DateField(blank=True, max_length=100, verbose_name='Date Initial')),
                ('dt_end', models.DateField(blank=True, max_length=100, verbose_name='Date End')),
                ('dt_renovation', models.DateField(blank=True, max_length=100, verbose_name='Date Renovation')),
                ('pdf_contract', models.FileField(blank=True, max_length=200, upload_to='contract/', verbose_name='File')),
                ('value', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Contract Value')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contract_company_created_id', to='company.company', verbose_name='Company')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contract_provider_created_id', to='provider.provider', verbose_name='Provider')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contract_status_created_id', to='status.status', verbose_name='Status')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contract_type_created_id', to='service_type.servicetype', verbose_name='Type')),
                ('user_created', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='contract_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('user_updated', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='contract_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'verbose_name': 'Contract',
                'verbose_name_plural': 'Contracts',
                'ordering': ['name'],
            },
        ),
    ]
