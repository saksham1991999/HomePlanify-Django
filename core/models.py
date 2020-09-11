from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime

type_choices = (
    ('B', 'Buy'),
    ('S', 'Sell'),
    ('R', 'Rent'),
)
"""
Builder floor,
Residential plot
Commercial 
"""
construction_choices = (
    ('RM', 'Ready to Move'),
    ('UC', 'Under Construction'),
)


class User(AbstractUser):
    is_agent = models.BooleanField(default=False)
    mobile = models.CharField(max_length=10)
    mobile_verified = models.BooleanField(default=False)
    profile_pic = models.ImageField(blank = True, null = True)

    def __str__(self):
        return self.username

class features(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title.capitalize()

    class Meta:
        verbose_name_plural = 'Features'

class FeaturedProperty(models.Model):
    name = models.CharField(max_length = 128)
    location = models.CharField(max_length = 128)
    description = models.TextField()
    image = models.ImageField()

    class Meta:
        verbose_name_plural = 'Featured Properties'

class property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices=type_choices, max_length=1)
    property_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    rooms = models.PositiveSmallIntegerField()

    construction_status = models.CharField(choices=construction_choices, max_length=2, blank=True, null = True)
    available_from = models.DateField(blank=True, null=True)
    price_sq = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()
    additional_features = models.TextField(blank = True, null = True)


    visible = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length = 10, null=True, blank=True)
    dateadded = models.DateField(auto_now_add=True)

    main_image = models.ImageField()
    features = models.ManyToManyField(features)
    youtube_video = models.CharField(max_length=512, blank=True, null=True, verbose_name='Youtube Video ID')
    youtube_video_2 = models.CharField(max_length=512, blank=True, null=True, verbose_name='Youtube 2nd Video ID')
    video = models.FileField(blank=True, null=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.property_name

    class Meta:
        verbose_name_plural = 'Properties'

    # def get_label(self):
    #     if self.label:
    #         return self.label
    #     else:
    #         return None

class images(models.Model):
    image = models.ImageField()
    property = models.ForeignKey(property, on_delete=models.CASCADE)

    def __str__(self):
        return self.property.property_name

    class Meta:
        verbose_name_plural = 'Images'

class agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    image = models.ImageField()

class Compare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    properties = models.ManyToManyField(property)

    def get_properties(self):
        properties_compare = self.properties.all()[:4]
        return properties_compare

    def __str__(self):
        return self.user.username

class bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    properties = models.ManyToManyField(property)

    def __str__(self):
        return self.user.username

class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name

class enquiry(models.Model):
    property = models.ForeignKey(property, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=10)
    subject = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Property Enquiries'

class mainenquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=10)
    subject = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Main Enquiries'

class District(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField()

    def get_no_of_areas(self):
        total = Area.objects.filter(district=self).count()
        return total

class Area(models.Model):
    district = models.ForeignKey('core.District', on_delete=models.PROTECT)
    title = models.CharField(max_length=256)
    image = models.ImageField()

class Banner(models.Model):
    title = models.CharField(max_length = 128)
    description = models.TextField()
    image = models.ImageField()
    link = models.CharField(max_length = 512)