# Generated by Django 3.2 on 2021-07-04 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0021_auto_20210704_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='number_months',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Number of Months'),
        ),
    ]
