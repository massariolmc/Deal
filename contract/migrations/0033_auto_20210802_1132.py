# Generated by Django 3.2 on 2021-08-02 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0032_alter_contract_pay_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nimbicontract',
            name='number_cod_nimbi',
            field=models.CharField(blank=True, max_length=100, verbose_name='Number PC Nimbi'),
        ),
        migrations.AlterField(
            model_name='nimbicontract',
            name='number_pc_nimbi',
            field=models.CharField(blank=True, max_length=100, verbose_name='Number PC SAP'),
        ),
        migrations.AlterField(
            model_name='nimbicontract',
            name='number_req_nimbi',
            field=models.CharField(max_length=100, verbose_name='Number Requisition Nimbi'),
        ),
    ]