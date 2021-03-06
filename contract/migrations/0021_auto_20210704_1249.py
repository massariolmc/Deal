# Generated by Django 3.2 on 2021-07-04 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0020_alter_contractcompany_contract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='number_months',
            field=models.PositiveIntegerField(blank=True, verbose_name='Number of Months'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='value_month',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, verbose_name='Value Month'),
        ),
    ]
