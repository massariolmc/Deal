# Generated by Django 3.2 on 2021-06-10 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contract', '0002_auto_20210610_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Slug')),
                ('dt_issue', models.DateField(blank=True, max_length=100, verbose_name='Issue Date')),
                ('number_invoice', models.CharField(max_length=100, verbose_name='Number Invoice')),
                ('ref_month', models.DateField(max_length=100, verbose_name='Reference Month')),
                ('value', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Invoice Value')),
                ('pay_day', models.DateField(blank=True, max_length=100, verbose_name='Payment Day')),
                ('telecom_data', models.CharField(blank=True, max_length=100, verbose_name='Telecom Data')),
                ('time_start', models.DateField(blank=True, max_length=100, verbose_name='Time Start')),
                ('time_end', models.DateField(blank=True, max_length=100, verbose_name='Time End')),
                ('forfeit_satus', models.CharField(blank=True, choices=[(True, 'Yes'), (False, 'No')], max_length=100, verbose_name='Forfeit Status')),
                ('value_forfeit', models.DecimalField(blank=True, decimal_places=2, max_digits=12, verbose_name='Value Forfeit')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('pdf_invoice', models.FileField(blank=True, max_length=200, upload_to='tax_invoice/', verbose_name='File')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tax_invoice_contract_created_id', to='contract.contract', verbose_name='Contract')),
                ('user_created', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='tax_invoice_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('user_updated', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='tax_invoice_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'verbose_name': 'Tax Invoice',
                'verbose_name_plural': 'Tax Invoices',
                'ordering': ['created_at'],
            },
        ),
    ]
