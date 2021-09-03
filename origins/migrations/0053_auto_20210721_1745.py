# Generated by Django 3.2.5 on 2021-07-21 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0052_turkanafossil_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='turkanafossil',
            name='in_origins',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='turkanafossil',
            name='in_turkana',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='turkanafossil',
            name='suffix_assigned',
            field=models.BooleanField(null=True),
        ),
    ]