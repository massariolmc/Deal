# Generated by Django 3.2 on 2021-06-18 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0006_alter_contract_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='dt_conclusion',
            field=models.DateField(blank=True, max_length=100, verbose_name='Date End'),
        ),
    ]