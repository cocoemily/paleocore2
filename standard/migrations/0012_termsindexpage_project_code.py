# Generated by Django 2.2.13 on 2020-07-13 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0011_term_is_subclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='termsindexpage',
            name='project_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='standard.Project'),
        ),
    ]