# Generated by Django 2.2.24 on 2021-07-06 18:04

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('site', models.CharField(max_length=255, null=True, verbose_name='Site name')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='Country')),
                ('data_source', models.CharField(blank=True, max_length=50, null=True, verbose_name='Data Source')),
                ('altitude', models.FloatField(blank=True, null=True, verbose_name='Altitude')),
                ('site_type', models.CharField(blank=True, choices=[('Shelter', 'Shelter'), ('Cave', 'Cave'), ('Open-air', 'Open-air'), ('Unknown', 'Unknown')], max_length=20, null=True, verbose_name='Site type')),
                ('display', models.NullBooleanField(verbose_name='Flagged')),
                ('map_location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layer', models.CharField(blank=True, max_length=300, null=True, verbose_name='Layer')),
                ('industry', models.CharField(blank=True, max_length=100, null=True, verbose_name='Industry')),
                ('industry_2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Industry')),
                ('industry_3', models.CharField(blank=True, max_length=100, null=True, verbose_name='Industry')),
                ('cat_no', models.CharField(blank=True, max_length=100, null=True, verbose_name='Catalog Number')),
                ('date', models.FloatField(blank=True, null=True, verbose_name='Age')),
                ('sd_plus', models.FloatField(blank=True, null=True, verbose_name='SD Plus')),
                ('sd_minus', models.FloatField(blank=True, null=True, verbose_name='SD Minus')),
                ('sample', models.CharField(blank=True, max_length=100, null=True, verbose_name='Sample')),
                ('technique', models.CharField(blank=True, max_length=100, null=True, verbose_name='Method')),
                ('corrected_date_BP', models.FloatField(blank=True, null=True, verbose_name='Cal. Age BP')),
                ('plus', models.FloatField(blank=True, null=True, verbose_name='Cal. Plus')),
                ('minus', models.FloatField(blank=True, null=True, verbose_name='Cal. Minus')),
                ('hominid_remains', models.TextField(blank=True, null=True, verbose_name='Hominins')),
                ('bibliography', models.TextField(blank=True, null=True, verbose_name='Bibliography')),
                ('period', models.CharField(blank=True, max_length=100, null=True, verbose_name='Period')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('intcal09_max', models.FloatField(blank=True, null=True, verbose_name='IntCal09 Max. Age')),
                ('intcal09_min', models.FloatField(blank=True, null=True, verbose_name='IntCal09 Min. Age')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paleosites.Site')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Site_plus_dates',
            fields=[
            ],
            options={
                'verbose_name': 'Sites and dates',
                'verbose_name_plural': 'Sites and dates',
                'managed': True,
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('paleosites.site',),
        ),
    ]