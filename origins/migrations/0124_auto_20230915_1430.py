# Generated by Django 3.2.18 on 2023-09-15 14:30

from django.db import migrations
import pandas as pd
from django.conf import settings
import os

source_path = os.path.join(settings.PROJECT_ROOT, 'origins','data','skeletal_elements.xlsx')
def import_data(source=source_path):
    xls = pd.ExcelFile(source)
    df = xls.parse(xls.sheet_names[0])
    return df

def import_skeletal_elements(apps, schema_editor):
    data = import_data()
    SkeletalElement = apps.get_model('origins', 'SkeletalElement')
    for i in data.index:
        name = data.loc[i].element_name # get the skeletal element name
        uberon_id = data.loc[i].uberon_id
        anatomical_region = data.loc[i].anatomical_region
        new_skeletal_element = SkeletalElement(name=name,
                                               uberon_id=uberon_id,
                                               anatomical_region=anatomical_region)
        new_skeletal_element.save()
class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0123_skeletalelement'),
    ]

    operations = [
        migrations.RunPython(import_skeletal_elements, reverse_code=migrations.RunPython.noop),
    ]