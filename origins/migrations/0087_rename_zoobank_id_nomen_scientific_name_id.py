# Generated by Django 3.2.5 on 2022-01-07 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0086_auto_20220107_1753'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nomen',
            old_name='zoobank_id',
            new_name='scientific_name_id',
        ),
    ]