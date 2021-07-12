# Generated by Django 3.2 on 2021-07-12 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0026_alter_contract_pay_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='dt_renovation',
            field=models.DateField(blank=True, help_text='Date renovatation or date readjustment yearly', max_length=100, null=True, verbose_name='Date Renovation'),
        ),
    ]
