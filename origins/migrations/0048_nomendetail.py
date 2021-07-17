# Generated by Django 2.2.24 on 2021-07-14 19:00

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('origins', '0047_auto_20210714_0432'),
    ]

    operations = [
        migrations.CreateModel(
            name='NomenDetail',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', models.CharField(blank=True, max_length=255)),
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
                ('body', wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('html', wagtail.core.blocks.RawHTMLBlock())])),
                ('template_string', models.CharField(choices=[('origins/nomina_list_view.html', 'Default Template')], default='pages/standard_page.html', max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]