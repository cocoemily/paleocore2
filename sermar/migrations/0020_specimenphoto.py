# Generated by Django 3.2.18 on 2023-10-28 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sermar', '0019_auto_20231027_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecimenPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/images/sermar', verbose_name='Image')),
                ('description', models.TextField(blank=True, null=True)),
                ('default_image', models.BooleanField(default=False)),
                ('occurrence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sermar.occurrence')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'managed': True,
            },
        ),
    ]
