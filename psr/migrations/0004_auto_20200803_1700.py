# Generated by Django 2.2.13 on 2020-08-03 17:00

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psr', '0003_auto_20200714_1932'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bone',
            fields=[
                ('archaeology_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='psr.Archaeology')),
                ('cutmarks', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'PSR Archaeological Fauna',
                'verbose_name_plural': 'PSR Archaeological Fauna',
            },
            bases=('psr.archaeology',),
        ),
        migrations.CreateModel(
            name='Cave',
            fields=[
                ('locality_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='psr.Locality')),
                ('find_type', models.CharField(blank=True, max_length=255, null=True)),
                ('dip', models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True)),
                ('strike', models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True)),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
                ('texture', models.CharField(blank=True, max_length=255, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True)),
                ('width', models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True)),
                ('depth', models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True)),
                ('slope_character', models.TextField(blank=True, max_length=64000, null=True)),
                ('sediment_presence', models.BooleanField(default=False)),
                ('sediment_character', models.TextField(blank=True, max_length=64000, null=True)),
                ('cave_mouth_character', models.TextField(blank=True, max_length=64000, null=True)),
                ('rockfall_character', models.TextField(blank=True, max_length=64000, null=True)),
                ('speleothem_character', models.TextField(blank=True, max_length=64000, null=True)),
            ],
            options={
                'verbose_name': 'PSR Cave/Rockshelter',
                'verbose_name_plural': 'PSR Caves/Rockshelters',
            },
            bases=('psr.locality',),
        ),
        migrations.CreateModel(
            name='Ceramic',
            fields=[
                ('archaeology_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='psr.Archaeology')),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'PSR Ceramic',
                'verbose_name_plural': 'PSR Ceramic',
            },
            bases=('psr.archaeology',),
        ),
        migrations.CreateModel(
            name='Lithic',
            fields=[
                ('archaeology_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='psr.Archaeology')),
                ('dataclass', models.CharField(blank=True, max_length=255, null=True)),
                ('fbtype', models.SmallIntegerField(blank=True, null=True)),
                ('form', models.CharField(blank=True, max_length=255, null=True)),
                ('technique', models.CharField(blank=True, max_length=255, null=True)),
                ('cortex', models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True)),
                ('coretype', models.CharField(blank=True, max_length=255, null=True)),
                ('platsurf', models.CharField(blank=True, max_length=255, null=True)),
                ('scarmorph', models.CharField(blank=True, max_length=255, null=True)),
                ('edgedamage', models.CharField(blank=True, max_length=255, null=True)),
                ('platwidth', models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True)),
                ('platthick', models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True)),
                ('epa', models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True)),
                ('scarlength', models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True)),
            ],
            options={
                'verbose_name': 'PSR Lithic',
                'verbose_name_plural': 'PSR Lithics',
            },
            bases=('psr.archaeology',),
        ),
        migrations.RemoveField(
            model_name='occurrence',
            name='item_scientific_name',
        ),
        migrations.AddField(
            model_name='aggregate',
            name='bone',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='aggregate',
            name='burning',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='aggregate',
            name='microfauna',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='aggregate',
            name='pebbles',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='aggregate',
            name='smalldebris',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True),
        ),
        migrations.AddField(
            model_name='aggregate',
            name='smallplatforms',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True),
        ),
        migrations.AddField(
            model_name='aggregate',
            name='tinydebris',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True),
        ),
        migrations.AddField(
            model_name='aggregate',
            name='tinyplatforms',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True),
        ),
        migrations.AddField(
            model_name='archaeology',
            name='archaeology_notes',
            field=models.TextField(blank=True, max_length=64000, null=True),
        ),
        migrations.AddField(
            model_name='archaeology',
            name='thick_mm',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True),
        ),
        migrations.AddField(
            model_name='archaeology',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='prism',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=38, null=True),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='problem_remarks',
            field=models.TextField(blank=True, max_length=64000, null=True),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='specimen_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Item ID'),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='suffix',
            field=models.IntegerField(blank=True, null=True, verbose_name='Suffix'),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='problem',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ExcavationUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=6)),
                ('extent', django.contrib.gis.db.models.fields.GeometryField(blank=True, dim=3, null=True, srid=4326)),
                ('locality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='psr.Locality')),
            ],
            options={
                'verbose_name': 'PSR Excavation Unit',
                'verbose_name_plural': 'PSR Excavation Units',
            },
        ),
        migrations.AddField(
            model_name='occurrence',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='psr.ExcavationUnit'),
        ),
    ]
