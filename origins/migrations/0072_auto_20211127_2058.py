# Generated by Django 3.2.5 on 2021-11-27 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0071_auto_20211127_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='context',
            name='problem_comment',
            field=models.TextField(blank=True, help_text='Description of the problem.', null=True),
        ),
        migrations.AlterField(
            model_name='fossil',
            name='problem_comment',
            field=models.TextField(blank=True, help_text='Description of the problem.', null=True),
        ),
        migrations.AlterField(
            model_name='identificationqualifier',
            name='problem_comment',
            field=models.TextField(blank=True, help_text='Description of the problem.', null=True),
        ),
        migrations.AlterField(
            model_name='nomen',
            name='problem_comment',
            field=models.TextField(blank=True, help_text='Description of the problem.', null=True),
        ),
        migrations.AlterField(
            model_name='site',
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
        migrations.AlterField(
            model_name='ttaxon',
            name='problem_comment',
            field=models.TextField(blank=True, help_text='Description of the problem.', null=True),
        ),
    ]
