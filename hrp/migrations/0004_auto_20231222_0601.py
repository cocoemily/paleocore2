# Generated by Django 3.2.23 on 2023-12-22 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrp', '0003_auto_20231221_1754'),
    ]

    operations = [
        migrations.RenameField(
            model_name='occurrence',
            old_name='recorded_by',
            new_name='collector_person',
        ),
        migrations.RenameField(
            model_name='occurrence',
            old_name='found_by',
            new_name='finder_person',
        ),
    ]