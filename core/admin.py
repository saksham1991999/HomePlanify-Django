from django.contrib import admin
from . import models


admin.site.site_header = 'HomePlanify'

class ImagesInlineAdmin(admin.TabularInline):
    model = models.images

class InquiryInlineAdmin(admin.TabularInline):
    model = models.enquiry
    extra = 0

class PropertyAdmin(admin.ModelAdmin):
    inlines = [ImagesInlineAdmin, InquiryInlineAdmin]

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


class AreaInlineAdmin(admin.TabularInline):
    model = models.Area
    extra = 3

class DistrictAdmin(admin.ModelAdmin):
    inlines = [AreaInlineAdmin]

admin.site.register(models.User)
admin.site.register(models.property, PropertyAdmin)
admin.site.register(models.images)

admin.site.register(models.features)
admin.site.register(models.contact)
admin.site.register(models.bookmark)
admin.site.register(models.Compare)
admin.site.register(models.enquiry)

admin.site.register(models.District, DistrictAdmin)
admin.site.register(models.Area)
admin.site.register(models.Banner)
admin.site.register(models.FeaturedProperty)
admin.site.register(models.InvestProperties)
