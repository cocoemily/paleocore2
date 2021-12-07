# Generated by Django 3.2.5 on 2021-11-08 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sermar', '0013_locality_protected_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locality',
            name='protected_area',
            field=models.CharField(blank=True, choices=[('Grumeti Game Reserve', 'Grumeti Game Reserve'), ('Ikorongo Game Reserve', 'Ikorongo Game Reserve'), ('Koyaki Group Ranch', 'Koyaki Group Ranch'), ('Lemek Group Ranch', 'Lemek Group Ranch'), ('Loliondo Game Control Area', 'Loliondo Game Control Area'), ('Masai Mara National Park', 'Masai Mara National Park'), ('Maswa Game Reserve', 'Maswa Game Reserve'), ('Ngorongoro Conservation Area', 'Ngorongoro Conservation Area'), ('Ol Choro Orogwa Group Ranch', 'Ol Choro Orogwa Group Ranch'), ('Olkinyei Group Ranch', 'Olkinyei Group Ranch'), ('Serengeti National Park', 'Serengeti National Park'), ('Siana Group Ranch', 'Siana Group Ranch'), ('Tarangire National Park', 'Tarangire National Park')], max_length=255, null=True),
        ),
    ]