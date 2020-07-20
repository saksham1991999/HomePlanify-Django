from django.contrib import admin
from . import models


admin.site.site_header = 'Huda Haryana'

class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'owner',
        'property_name',
        'city',
        'visible',
        'verified',
                    ]
    list_display_links = [
        'id',
        'owner',
        'property_name',
    ]
    list_filter = [
        'property_name',
        'city',
        'visible',
        'verified',
        'additional_features',
    ]
    search_fields = [
                    'owner',
                    'property_name',
                    'city',
                    'features',
    ]

class ImagesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'owner',
        'property_name',
        'city',
        'visible',
        'verified',
                    ]
    list_display_links = [
        'id',
        'owner',
        'property_name',
    ]
    list_filter = [
        'property_name',
        'city',
        'visible',
        'verified',
        'additional_features',
    ]
    search_fields = [
                    'owner',
                    'property_name',
                    'city',
                    'features',
    ]


admin.site.register(models.User)
admin.site.register(models.property, PropertyAdmin)
admin.site.register(models.images)

admin.site.register(models.features)
admin.site.register(models.contact)
admin.site.register(models.bookmark)
admin.site.register(models.Compare)
admin.site.register(models.enquiry)

admin.site.register(models.District)
admin.site.register(models.Area)