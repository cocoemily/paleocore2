# Generated by Django 3.2.15 on 2022-10-01 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0095_alter_nomen_status_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomen',
            name='type_specimen_status',
            field=models.CharField(blank=True, choices=[('holotype', 'Holotype'), ('paratype', 'Paratype'), ('lectotype', 'Lectotype'), ('neotype', 'Neotype'), ('syntype', 'Syntype')], max_length=255, null=True),
        ),
    ]