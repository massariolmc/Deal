# Generated by Django 3.2 on 2021-07-21 01:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contract', '0028_auto_20210720_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='dt_create_rc',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='dt_send_nf_fiscal',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='number_cod_nimbi',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='number_cod_project',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='number_cost_center',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='number_pc_nimbi',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='number_req_nimbi',
        ),
        migrations.CreateModel(
            name='NimbiContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_req_nimbi', models.CharField(blank=True, max_length=100, verbose_name='Number Requisition Nimbi')),
                ('number_cod_nimbi', models.CharField(blank=True, max_length=100, verbose_name='Number Cod Nimbi')),
                ('number_pc_nimbi', models.CharField(blank=True, max_length=100, verbose_name='Number PC Nimbi')),
                ('number_cod_project', models.CharField(blank=True, max_length=100, verbose_name='Number Cod Project')),
                ('number_cost_center', models.CharField(blank=True, max_length=100, verbose_name='Number Cost  Center')),
                ('dt_create_rc', models.DateField(blank=True, max_length=100, null=True, verbose_name='Create RC Date Nimbi')),
                ('dt_send_nf_fiscal', models.DateField(blank=True, max_length=100, null=True, verbose_name='Send Date Fiscal')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nimbi_contract', to='contract.contract', verbose_name='Contract')),
                ('user_created', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='nimbi_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('user_updated', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='nimbi_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'verbose_name': 'Nimbi',
                'verbose_name_plural': 'Nimbi',
                'ordering': ['number_req_nimbi'],
            },
        ),
    ]
