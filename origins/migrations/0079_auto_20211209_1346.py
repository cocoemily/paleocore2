# Generated by Django 3.2.5 on 2021-12-09 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0078_auto_20211209_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turkanafossil',
            name='to_split',
        ),
        migrations.AddField(
            model_name='fossil',
            name='to_split',
            field=models.BooleanField(null=True),
        ),
    ]
