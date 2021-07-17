# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-08-04 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eval', '0002_auto_20200512_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='gender_pronouns',
            field=models.CharField(blank=True, choices=[('he/him/his', 'he'), ('she/her/hers', 'her'), ('they/them/theirs', 'they')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='incoming_degree',
            field=models.TextField(blank=True, choices=[('BA', 'BA'), ('MA', 'MA')], max_length=100, null=True),
        ),
    ]