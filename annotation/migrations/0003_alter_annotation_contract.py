# Generated by Django 3.2 on 2021-07-01 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0016_auto_20210630_2230'),
        ('annotation', '0002_alter_annotation_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotation_contract_created_id', to='contract.contract', verbose_name='Contract'),
        ),
    ]
