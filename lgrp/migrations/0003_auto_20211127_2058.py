# Generated by Django 3.2.5 on 2021-11-27 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lgrp', '0002_auto_20200612_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectioncode',
            name='problem_comment',
            field=models.TextField(blank=True, help_text='Description of the problem.', null=True),
        ),
        migrations.AlterField(
            model_name='identificationqualifier',
            name='problem_comment',
            field=models.TextField(blank=True, help_text='Description of the problem.', null=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='problem_comment',
            field=models.TextField(blank=True, help_text='Description of the problem.', null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='problem_comment',
            field=models.TextField(blank=True, help_text='Description of the problem.', null=True),
        ),
        migrations.AlterField(
            model_name='stratigraphicunit',
            name='problem_comment',
            field=models.TextField(blank=True, help_text='Description of the problem.', null=True),
        ),
        migrations.AlterField(
            model_name='taxon',
            name='problem_comment',
            field=models.TextField(blank=True, help_text='Description of the problem.', null=True),
        ),
        migrations.AlterField(
            model_name='taxonrank',
            name='problem_comment',
            field=models.TextField(blank=True, help_text='Description of the problem.', null=True),
        ),
    ]
