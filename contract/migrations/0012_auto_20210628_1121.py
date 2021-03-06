# Generated by Django 3.2 on 2021-06-28 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0002_company_status'),
        ('contract', '0011_uploadcontract_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contract_company_company_created_id', to='company.company', verbose_name='Company')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contract_company_contract_created_id', to='contract.contract', verbose_name='Contract')),
                ('user_created', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='contract_company_cc_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('user_updated', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='contract_company_cc_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'verbose_name': 'Contract Company',
                'verbose_name_plural': 'Contract Companies',
                'ordering': ['updated_at'],
            },
        ),
        migrations.AddField(
            model_name='contract',
            name='members_contract',
            field=models.ManyToManyField(through='contract.ContractCompany', to='company.Company'),
        ),
    ]
