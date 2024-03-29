# Generated by Django 3.2.5 on 2021-10-01 23:08

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0059_auto_20211001_2259'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fossil',
            options={},
        ),
        migrations.AddField(
            model_name='fossil',
            name='georeference_remarks',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='fossil',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fossil',
            name='short_description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
