# Generated by Django 3.2.18 on 2023-05-18 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_alter_projectpage_app_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectpage',
            name='app_label',
            field=models.CharField(blank=True, choices=[('compressor', 'compressor'), ('joyous', 'joyous'), ('mptt', 'mptt'), ('rest_framework', 'rest_framework'), ('publications', 'publications'), ('projects', 'projects'), ('standard', 'standard'), ('drp', 'drp'), ('mlp', 'mlp'), ('hrp', 'hrp'), ('lgrp', 'lgrp'), ('eppe', 'eppe'), ('gdb', 'gdb'), ('omo_mursi', 'omo_mursi'), ('origins', 'origins'), ('psr', 'psr'), ('cc', 'cc'), ('fc', 'fc'), ('wtap', 'wtap'), ('arvrc', 'arvrc'), ('eval', 'eval'), ('paleosites', 'paleosites'), ('turkana', 'turkana'), ('sermar', 'sermar'), ('utcasts', 'utcasts'), ('wormil', 'wormil'), ('inca', 'inca'), ('idit', 'idit')], max_length=100, null=True),
        ),
    ]
