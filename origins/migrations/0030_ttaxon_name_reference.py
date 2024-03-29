# Generated by Django 2.2.19 on 2021-05-03 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0003_auto_20210326_2356'),
        ('origins', '0029_remove_ttaxon_name_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='ttaxon',
            name='name_reference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='name_references', to='publications.Publication'),
        ),
    ]
