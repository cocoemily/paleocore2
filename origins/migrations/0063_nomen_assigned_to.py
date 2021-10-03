# Generated by Django 3.2.5 on 2021-10-02 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0062_rename_type_object_nomen_type_specimen'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomen',
            name='assigned_to',
            field=models.CharField(blank=True, choices=[('Denne Reed', 'DR'), ('Emily Raney', 'ER'), ('Jyhreh Johnson', 'JJ'), ('Harper Jackson', 'HJ'), ('Nida Virabalin', 'NV')], max_length=255, null=True),
        ),
    ]