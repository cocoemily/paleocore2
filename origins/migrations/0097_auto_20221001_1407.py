# Generated by Django 3.2.15 on 2022-10-01 14:07

from django.db import migrations


def copy_type_status_data(apps, schema_editor):
    Nomen = apps.get_model('origins', 'Nomen')
    for nomen in Nomen.objects.all():
        try:
            nomen.type_specimen_status = nomen.type_specimen.type_status
            nomen.save()
        # If a nomen lacks a type specimen we may encounter None which will raise an Attribute Error
        except AttributeError:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0096_nomen_type_specimen_status'),
    ]

    operations = [
        migrations.RunPython(copy_type_status_data)
    ]
