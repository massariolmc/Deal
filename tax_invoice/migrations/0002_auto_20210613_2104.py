# Generated by Django 3.2 on 2021-06-14 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax_invoice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxinvoice',
            name='dt_issue',
            field=models.DateField(blank=True, max_length=100, null=True, verbose_name='Issue Date'),
        ),
        migrations.AlterField(
            model_name='taxinvoice',
            name='forfeit_satus',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=100, verbose_name='Forfeit Status'),
        ),
        migrations.AlterField(
            model_name='taxinvoice',
            name='pay_day',
            field=models.DateField(blank=True, max_length=100, null=True, verbose_name='Payment Day'),
        ),
        migrations.AlterField(
            model_name='taxinvoice',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Invoice Value'),
        ),
        migrations.AlterField(
            model_name='taxinvoice',
            name='value_forfeit',
            field=models.DecimalField(blank=True, decimal_places=2, default='0,00', max_digits=20, verbose_name='Value Forfeit'),
        ),
    ]
