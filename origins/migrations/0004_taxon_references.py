# Generated by Django 2.2.13 on 2020-10-30 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0002_initial_data'),
        ('origins', '0003_site_references'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxon',
            name='references',
            field=models.ManyToManyField(blank=True, to='publications.Publication'),
        ),
    ]
