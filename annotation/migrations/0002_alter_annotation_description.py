# Generated by Django 3.2 on 2021-06-23 02:36

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Description'),
        ),
    ]
