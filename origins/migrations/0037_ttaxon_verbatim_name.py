# Generated by Django 2.2.19 on 2021-05-15 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0036_auto_20210504_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='ttaxon',
            name='verbatim_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]