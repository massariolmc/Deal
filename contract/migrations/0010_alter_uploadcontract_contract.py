# Generated by Django 3.2 on 2021-06-24 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0009_auto_20210624_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadcontract',
            name='contract',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='upload_contract_contract_created_id', to='contract.contract', verbose_name='Contract'),
        ),
    ]
