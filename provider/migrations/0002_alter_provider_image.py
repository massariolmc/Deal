# Generated by Django 3.2 on 2021-06-02 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='image',
            field=models.ImageField(blank=True, max_length=200, upload_to='provider/', verbose_name='Image'),
        ),
    ]
