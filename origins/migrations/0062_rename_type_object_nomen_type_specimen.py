# Generated by Django 3.2.5 on 2021-10-02 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0061_rename_type_specimen_nomen_type_specimen_label'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nomen',
            old_name='type_object',
            new_name='type_specimen',
        ),
    ]