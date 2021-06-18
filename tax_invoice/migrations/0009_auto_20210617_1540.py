# Generated by Django 3.2 on 2021-06-17 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax_invoice', '0008_alter_taxinvoice_pay_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxinvoice',
            name='dt_create_rc',
            field=models.DateField(blank=True, default='1950-01-01', max_length=100, verbose_name='Create RC Date Nimbi'),
        ),
        migrations.AddField(
            model_name='taxinvoice',
            name='dt_send_nf_fiscal',
            field=models.DateField(blank=True, default='1950-01-01', max_length=100, verbose_name='Send Date Fiscal'),
        ),
        migrations.AddField(
            model_name='taxinvoice',
            name='number_cod_nimbi',
            field=models.CharField(blank=True, default='0', max_length=100, verbose_name='Number Cod Nimbi'),
        ),
        migrations.AddField(
            model_name='taxinvoice',
            name='number_cod_project',
            field=models.CharField(blank=True, default='0', max_length=100, verbose_name='Number Cod Project'),
        ),
        migrations.AddField(
            model_name='taxinvoice',
            name='number_cost_center',
            field=models.CharField(blank=True, default='0', max_length=100, verbose_name='Number Cost  Center'),
        ),
        migrations.AddField(
            model_name='taxinvoice',
            name='number_pc_nimbi',
            field=models.CharField(blank=True, default='0', max_length=100, verbose_name='Number PC Nimbi'),
        ),
        migrations.AddField(
            model_name='taxinvoice',
            name='number_req_nimbi',
            field=models.CharField(blank=True, default='0', max_length=100, verbose_name='Number Requisition Nimbi'),
        ),
        migrations.AlterField(
            model_name='taxinvoice',
            name='pay_day',
            field=models.DateField(blank=True, max_length=100, verbose_name='Payment Day'),
        ),
    ]