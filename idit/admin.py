from django.contrib import admin
from .models import Character, CharacterState, CharacterStateImage, Description, Species, ItemImage, Item


class CharacterStateImageInline(admin.TabularInline):
    model = CharacterStateImage
    extra = 0


class CharacterStateAdmin(admin.ModelAdmin):
    inlines = [CharacterStateImageInline]
    ordering = ['cs']


class CharacterStateInline(admin.TabularInline):
    model = CharacterState
    readonly_fields = ['cs_thumbnail']
    fields = ['id', 'cs', 'name', 'cs_thumbnail', 'implicit', 'use_edit', 'use_identify']
    ordering = ['cs']
    show_change_link = True


class CharacterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'unit', 'notes', 'type', 'mandatory', 'element', 'disabled']
    list_filter = ['type', 'element', 'disabled', 'mandatory']
    inlines = [CharacterStateInline]
    fieldsets = (
        ('General', {
            'fields': [('name',),
                       ('disabled', 'mandatory'),
                       ('element',),
                       ('type', 'multistate_type'),
                       ('unit', 'unit_is_prefix'),
                       ('reliability', 'availability', 'fuzziness', 'fuzziness_is_percent'),
                       ('heading', 'heading_link'),
                       ('wording',),
                       ('alternate_wording',),
                       ('notes',),
                       ],
        }),
    )


class DescriptionInline(admin.TabularInline):
    model = Description
    ordering = ['character']
    #fields = ['character', 'character_state', 'x']
    fields = ['character_state']
    # select_related = True
    extra = 1

    # def get_queryset(self, request):
    #     return super(DescriptionInline, self).get_queryset(request). \
    #         prefetch_related('character_state__character')


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    readonly_fields = ['photo', 'thumbnail']
    fieldsets = (
        ('Photos', {
            'fields': [('default_image', 'image', 'thumbnail', 'description')],
            'classes': ['collapse']
        }),
    )


class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ['photo']
    list_display = ['name', 'notes', 'species', 'taxonomic_order', 'thumbnail']
    list_filter = ['taxonomic_order', 'collection_code']
    list_select_related = True
    inlines = [ItemImageInline, DescriptionInline]
    search_fields = ['name', 'wording', 'notes', 'collection_code', 'taxonomic_order']
    fieldsets = (
        ('General', {
            'fields': [('name', 'wording'),
                       ('notes', 'collection_code', 'collection_unit'),
                       ('abundance', 'species', 'taxonomic_order')],
        }),
    )


class DescriptionAdmin(admin.ModelAdmin):
    list_display = ['item', 'character', 'character_state', 'x']
    list_filter = ['item']


admin.site.register(Character, CharacterAdmin)
admin.site.register(CharacterState, CharacterStateAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Species)
admin.site.register(Description, DescriptionAdmin)
