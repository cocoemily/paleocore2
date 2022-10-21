from django.db import models
from django.utils.html import mark_safe
import os
from django.core.exceptions import ObjectDoesNotExist

CHARTYPE_CHOICES = (('UM', 'Unordered Multistate'), ('OM', 'Ordered Multistate'), ('IN', 'Integer'),
                    ('RN', 'Real Number'), ('TE', 'Text'))
ELEMENT_CHOICES = (('U', 'Upper Jaw'), ('L', 'Lower Jaw'), ('B', 'Both'))


class Collection(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    address = models.CharField(max_length=500, default='', null=True, blank=True)
    city = models.CharField(max_length=100, default='', null=True, blank=True)
    country = models.CharField(max_length=100, default='', null=True, blank=True)
    contact_name = models.CharField(max_length=100, default='', null=True, blank=True)
    contact_email = models.CharField(max_length=100, default='', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)


class Character(models.Model):
    name = models.CharField(max_length=50, default='', null=False)
    unit = models.CharField(max_length=5, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=5, default='UM', null=False, choices=CHARTYPE_CHOICES)
    mandatory = models.BooleanField(default=False, null=True, blank=True)
    multistate_type = models.IntegerField(default=1, null=False)
    reliability = models.IntegerField(default=5)
    availability = models.IntegerField(default=5)
    fuzziness = models.DecimalField(decimal_places=5, max_digits=20, default=0, null=False)
    fuzziness_is_percent = models.BooleanField(null=True, blank=True, default=False)
    key_states = models.CharField(max_length=5, null=True, blank=True)
    heading = models.IntegerField(null=True, blank=True)
    heading_link = models.IntegerField(null=True, blank=True)
    wording = models.TextField(null=True, blank=True)
    alternate_wording = models.TextField(null=True, blank=True)
    unit_is_prefix = models.BooleanField(null=True, blank=True, default=False)
    format_string = models.TextField(null=True, blank=True)
    paragraph_link = models.IntegerField(null=True, blank=True)
    sentence_link = models.IntegerField(null=True, blank=True)
    comma_link = models.IntegerField(null=True, blank=True)
    special_link = models.IntegerField(null=True, blank=True)
    special_element = models.IntegerField(null=True, blank=True)
    use_comma = models.BooleanField(null=True, blank=True, default=False)
    omit_final_comma = models.BooleanField(null=True, blank=True, default=False)
    omit_values = models.BooleanField(null=True, blank=True, default=False)
    emphasize = models.BooleanField(null=True, blank=True, default=False)
    omit_period = models.BooleanField(null=True, blank=True, default=False)
    num_states = models.IntegerField(default=2, null=True, blank=True)
    char_ref = models.IntegerField(null=True, blank=True)
    element = models.CharField(max_length=4,  default='U', null=True, blank=True, choices=ELEMENT_CHOICES)
    disabled = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name


class CharacterState(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    cs = models.CharField(max_length=30, null=False)
    name = models.CharField(max_length=100, null=False)
    notes = models.TextField(null=True, blank=True)
    wording = models.CharField(max_length=10, null=True, blank=True)
    format_string = models.CharField(max_length=10, null=True, blank=True)
    implicit = models.BooleanField(null=True, blank=True, default=False)
    use_edit = models.BooleanField(null=True, blank=True, default=True)
    use_identify = models.BooleanField(null=True, blank=True, default=False)
    use_description = models.BooleanField(null=True, blank=True, default=False)
    use_phylo = models.BooleanField(null=True, blank=True, default=False)
    use_other = models.BooleanField(null=True, blank=True, default=False)

    def cs_image(self):
        try:
            character_state_image_obj = self.characterstateimage_set.get(default_image=True)
            return character_state_image_obj.image()
        except ObjectDoesNotExist:
            return None

    def cs_thumbnail(self):
        try:
            character_state_image_obj = self.characterstateimage_set.get(default_image=True)
            return character_state_image_obj.thumbnail()
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return str(self.character.name) + ':' + self.name


class Species(models.Model):
    genus_name = models.CharField(max_length=50, null=False)
    trivial_name = models.CharField(max_length=50, null=False)
    common_name = models.CharField(max_length=50, null=True)
    type_citation = models.TextField(null=True)
    type_location_id = models.IntegerField(null=True)
    type_specimen_no = models.CharField(max_length=100, null=True)
    generic_type = models.BooleanField(null=True, blank=True)
    genus_citation = models.TextField(null=True)
    taxonomic_order = models.CharField(max_length=50, null=True)
    taxonomic_family = models.CharField(max_length=50, null=True)
    taxonomic_subfamily = models.CharField(max_length=50, null=True)
    notes = models.TextField(null=True)
    extant = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.genus_name + ' ' + self.trivial_name

    class Meta:
        verbose_name_plural = 'Species'


class Item(models.Model):
    name = models.CharField(max_length=100, null=False)
    wording = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    abundance = models.IntegerField(null=True, blank=True)
    collection_unit = models.CharField(max_length=50, null=True, blank=True)
    lit_ref = models.CharField(max_length=100, null=True, blank=True)
    lit_key = models.IntegerField(null=True, blank=True)
    lit_ref_detail = models.TextField(null=True, blank=True)
    collection_code = models.CharField(max_length=15, null=True, blank=True)
    specimen_no = models.CharField(max_length=20, null=True, blank=True)
    species = models.ForeignKey(Species, null=True, blank=True, on_delete=models.SET_NULL)
    taxonomic_order = models.CharField(max_length=50, null=True, blank=True)
    disabled = models.BooleanField(null=True, blank=True, default=False)
    image = models.ImageField(upload_to='Item_Images', null=True, blank=True)

    def __str__(self):
        return self.name

    def photo(self):
        try:
            img_src = os.path.join(self.image.url)
            return f'<a href="{img_src}"><img src="{img_src}" style="width:600px" /></a>'
        except ObjectDoesNotExist:
            return None

    photo.short_description = 'Photo'
    photo.allow_tags = True
    photo.mark_safe = True

    def thumbnail(self):
        try:
            thumb_img_src = os.path.join(self.image.url)
            return f'<a href="{thumb_img_src}"><img src="{thumb_img_src}" style="width:100px" /></a>'
        except ObjectDoesNotExist:
            return None
        except ValueError:
            return None

    thumbnail.short_description = 'Thumb'
    thumbnail.allow_tags = True
    thumbnail.mark_safe = True

    def item_images(self):
        return ItemImage.objects.filter(item=self.id)

    def item_photos(self):
        try:
            image_string = ''
            for i in self.item_images():
                iphotos_img_src = os.path.join(i.url)
                img_html_string = f'<a href={iphotos_img_src}><img src={iphotos_img_src} style="width:600px" /></a>'
                image_string += img_html_string
            return image_string
        except ObjectDoesNotExist:
            return None
        except ValueError:
            return None


class Description(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    modifier = models.CharField(max_length=10, null=True, blank=True)
    cs_value = models.CharField(max_length=10, null=True, blank=True)
    character_state = models.ForeignKey(CharacterState, null=True, blank=True, on_delete=models.SET_NULL)
    x = models.DecimalField(decimal_places=5, max_digits=20, default=0, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    sequence = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.item.__str__()+'['+self.character.__str__()+', '+self.cs_value+']'


class ItemImage(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)  # FK to item
    image = models.ImageField(upload_to='Item_Images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    default_image = models.BooleanField(default=False)

    def photo(self):
        try:
            photo_img_src = os.path.join(self.image.url)
            src_html = f'<a href="{photo_img_src}"><img src="{photo_img_src}" style="width:600px" /></a>'
            return mark_safe(src_html)
        except ObjectDoesNotExist:
            return None
        except ValueError:
            return None

    photo.short_description = 'Photo'
    photo.allow_tags = True
    photo.mark_safe = True

    def thumbnail(self):
        try:
            item_img_thumb_img_src = os.path.join(self.image.url)
            src_html = f'<a href="{item_img_thumb_img_src}"><img src="{item_img_thumb_img_src}" style="width:100px" /></a>'
            return mark_safe(src_html)
        except ValueError:
            return None
        except ObjectDoesNotExist:
            return None

    thumbnail.short_description = 'Thumb'
    thumbnail.allow_tags = True
    thumbnail.mark_safe = True


class CharacterStateImage(models.Model):
    cs = models.ForeignKey('CharacterState', on_delete=models.CASCADE)
    image = models.ImageField('Image', upload_to='CS_Images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    default_image = models.BooleanField(default=False)

    def photo(self):
        try:
            photo_img_src = os.path.join(self.image.url)
            src_html = f'<a href="{photo_img_src}"><img src="{photo_img_src}" style="width:600px" /></a>'
            return mark_safe(src_html)
        except ObjectDoesNotExist:
            return None
        except ValueError:
            return None

    photo.short_description = 'Photo'
    photo.allow_tags = True
    photo.mark_safe = True

    def thumbnail(self):
        try:
            cs_thumbnail_src = os.path.join(self.image.url)
            src_html = f'<a href="{cs_thumbnail_src}"><img src="{cs_thumbnail_src}" style="width:100px" /></a>'
            return mark_safe(src_html)
        except ValueError:
            return None
        except ObjectDoesNotExist:
            return None

    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True
    thumbnail.mark_safe = True

    class Meta:
        managed = True
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
