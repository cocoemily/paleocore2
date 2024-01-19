# Generated by Django 3.2.18 on 2023-11-18 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0126_ttaxon_nomen'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ttaxon',
            options={'verbose_name': 'TTaxon', 'verbose_name_plural': 'TTaxa'},
        ),
        migrations.RemoveField(
            model_name='ttaxon',
            name='authorship',
        ),
        migrations.RemoveField(
            model_name='ttaxon',
            name='epithet',
        ),
        migrations.RemoveField(
            model_name='ttaxon',
            name='verbatim_name',
        ),
        migrations.RemoveField(
            model_name='ttaxon',
            name='zoobank_id',
        ),
    ]