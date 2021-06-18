# Generated by Django 3.2 on 2021-06-18 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='status',
            field=models.CharField(choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo')], default='Ativo', max_length=100, verbose_name='Status'),
        ),
    ]
