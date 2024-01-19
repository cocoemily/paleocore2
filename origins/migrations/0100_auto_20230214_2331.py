# Generated by Django 3.2.15 on 2023-02-14 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0099_auto_20221104_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fossil',
            name='type_status',
        ),
        migrations.AddField(
            model_name='fossil',
            name='verbatim_turkana_fossil',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fossil',
            name='assigned_to',
            field=models.CharField(blank=True, choices=[('Denne Reed', 'DR'), ('Emily Raney', 'ER'), ('Jyhreh Johnson', 'JJ'), ('Harper Jackson', 'HJ'), ('Kennedy Knowlton', 'KK'), ('Nida Virabalin', 'NV'), ('Ashlynn Arzola', 'AA'), ('Nicholas Hartman', 'NH'), ('Jorge Ramirez Salinas', 'JRS'), ('Hayden Post', 'HP')], max_length=255, null=True, verbose_name='Assigned'),
        ),
        migrations.AlterField(
            model_name='fossil',
            name='is_type_specimen',
            field=models.BooleanField(default=False, verbose_name='Type specimen'),
        ),
        migrations.AlterField(
            model_name='fossil',
            name='verified_by',
            field=models.CharField(blank=True, choices=[('Denne Reed', 'DR'), ('Emily Raney', 'ER'), ('Jyhreh Johnson', 'JJ'), ('Harper Jackson', 'HJ'), ('Kennedy Knowlton', 'KK'), ('Nida Virabalin', 'NV'), ('Ashlynn Arzola', 'AA'), ('Nicholas Hartman', 'NH'), ('Jorge Ramirez Salinas', 'JRS'), ('Hayden Post', 'HP')], max_length=255, null=True, verbose_name='Verified'),
        ),
        migrations.AlterField(
            model_name='nomen',
            name='assigned_to',
            field=models.CharField(blank=True, choices=[('Denne Reed', 'DR'), ('Emily Raney', 'ER'), ('Jyhreh Johnson', 'JJ'), ('Harper Jackson', 'HJ'), ('Kennedy Knowlton', 'KK'), ('Nida Virabalin', 'NV'), ('Ashlynn Arzola', 'AA'), ('Nicholas Hartman', 'NH'), ('Jorge Ramirez Salinas', 'JRS'), ('Hayden Post', 'HP')], max_length=255, null=True, verbose_name='Assigned'),
        ),
        migrations.AlterField(
            model_name='nomen',
            name='verified_by',
            field=models.CharField(blank=True, choices=[('Denne Reed', 'DR'), ('Emily Raney', 'ER'), ('Jyhreh Johnson', 'JJ'), ('Harper Jackson', 'HJ'), ('Kennedy Knowlton', 'KK'), ('Nida Virabalin', 'NV'), ('Ashlynn Arzola', 'AA'), ('Nicholas Hartman', 'NH'), ('Jorge Ramirez Salinas', 'JRS'), ('Hayden Post', 'HP')], max_length=255, null=True, verbose_name='Verified'),
        ),
        migrations.AlterField(
            model_name='site',
            name='assigned_to',
            field=models.CharField(blank=True, choices=[('Denne Reed', 'DR'), ('Emily Raney', 'ER'), ('Jyhreh Johnson', 'JJ'), ('Harper Jackson', 'HJ'), ('Kennedy Knowlton', 'KK'), ('Nida Virabalin', 'NV'), ('Ashlynn Arzola', 'AA'), ('Nicholas Hartman', 'NH'), ('Jorge Ramirez Salinas', 'JRS'), ('Hayden Post', 'HP')], max_length=255, null=True, verbose_name='Assigned'),
        ),
        migrations.AlterField(
            model_name='site',
            name='verified_by',
            field=models.CharField(blank=True, choices=[('Denne Reed', 'DR'), ('Emily Raney', 'ER'), ('Jyhreh Johnson', 'JJ'), ('Harper Jackson', 'HJ'), ('Kennedy Knowlton', 'KK'), ('Nida Virabalin', 'NV'), ('Ashlynn Arzola', 'AA'), ('Nicholas Hartman', 'NH'), ('Jorge Ramirez Salinas', 'JRS'), ('Hayden Post', 'HP')], max_length=255, null=True, verbose_name='Verified'),
        ),
    ]