# Generated by Django 3.2.12 on 2022-05-13 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wormil', '0003_auto_20220513_0208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='specimen',
            old_name='finder',
            new_name='found_by',
        ),
    ]