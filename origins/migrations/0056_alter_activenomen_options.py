# Generated by Django 3.2.5 on 2021-07-29 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0055_alter_activenomen_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activenomen',
            options={'ordering': ['name'], 'verbose_name': 'Active Nomen', 'verbose_name_plural': 'Active Nomina'},
        ),
    ]
