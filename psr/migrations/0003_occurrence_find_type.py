# Generated by Django 2.2.13 on 2020-12-15 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psr', '0002_auto_20201209_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrence',
            name='find_type',
            field=models.CharField(blank=True, max_length=255, verbose_name='Find Type'),
        ),
    ]
