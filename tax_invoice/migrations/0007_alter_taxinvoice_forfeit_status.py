# Generated by Django 3.2 on 2021-06-16 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax_invoice', '0006_alter_taxinvoice_pay_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxinvoice',
            name='forfeit_status',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=100, verbose_name='Forfeit Status'),
        ),
    ]
