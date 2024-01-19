# Generated by Django 3.2.15 on 2023-02-15 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0100_auto_20230214_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='fossil',
            name='area',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='fossil',
            name='item_part',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='fossil',
            name='suffix_added',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='fossil',
            name='locality',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='fossil',
            name='place_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]