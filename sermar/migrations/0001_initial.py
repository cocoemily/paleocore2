# Generated by Django 3.2.5 on 2021-10-22 01:36

import ckeditor.fields
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, help_text='The date and time this resource was first created.', verbose_name='Created')),
                ('date_last_modified', models.DateTimeField(default=django.utils.timezone.now, help_text='The date and time this resource was last altered.', verbose_name='Modified')),
                ('problem', models.BooleanField(default=False, help_text='Is there a problem with this record that needs attention?')),
                ('problem_comment', models.TextField(blank=True, help_text='Description of the problem.', max_length=255, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, help_text='General remarks about this database record.', null=True, verbose_name='Record Remarks')),
                ('last_import', models.BooleanField(default=False)),
                ('georeference_remarks', models.TextField(blank=True, max_length=500, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('priority', models.IntegerField(blank=True, null=True)),
                ('verbatim_in_park', models.IntegerField(blank=True, null=True)),
                ('in_park', models.BooleanField(null=True)),
                ('owls', models.IntegerField(blank=True, null=True)),
                ('owl_species', models.CharField(blank=True, choices=[('Tyto alba', 'Tyto alba'), ('Bubo africanus', 'Bubo africanus'), ('Bubo lacteus', 'Bubo lacteus')], max_length=256, null=True)),
                ('verbatim_pellets', models.IntegerField(blank=True, null=True)),
                ('pellets', models.BooleanField(blank=True, null=True)),
                ('pellet_species', models.CharField(blank=True, choices=[('Tyto alba', 'Tyto alba'), ('Bubo africanus', 'Bubo africanus'), ('Bubo lacteus', 'Bubo lacteus')], max_length=256, null=True)),
                ('verbatim_bones', models.IntegerField(blank=True, null=True)),
                ('bones', models.BooleanField(null=True)),
                ('sample_size', models.IntegerField(blank=True, null=True)),
                ('landmark', models.CharField(blank=True, max_length=256, null=True)),
                ('verbatim_easting', models.IntegerField(blank=True, null=True)),
                ('verbatim_northing', models.IntegerField(blank=True, null=True)),
                ('verbatim_utm_zone', models.IntegerField(blank=True, null=True)),
                ('verbatim_roost_type', models.CharField(blank=True, max_length=256, null=True)),
                ('roost_type', models.CharField(blank=True, max_length=256, null=True)),
                ('adequate_sample', models.BooleanField(null=True)),
                ('verbatim_analysis', models.IntegerField(blank=True, null=True)),
                ('analysis', models.BooleanField(null=True)),
            ],
            options={
                'verbose_name': 'Locality',
                'verbose_name_plural': 'Localities',
            },
        ),
    ]
