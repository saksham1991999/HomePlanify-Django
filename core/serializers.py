# from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import User, property, images, bookmark, contact, enquiry, mainenquiry


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="user-detail")

    class Meta:
        model = User
        fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="property-detail")

    class Meta:
        model = property
        fields = "__all__"

class ImagesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="image-detail")

    class Meta:
        model = images
        fields = "__all__"

class BookmarkSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="bookmark-detail")

    class Meta:
        model = bookmark
        fields = "__all__"

class ContactSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="contact-detail")

    class Meta:
        model = contact
        fields = "__all__"

class EnquirySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="enquiry-detail")

    class Meta:
        model = enquiry
        fields = "__all__"

class MainEnquirySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="main-enquiry-detail")

    class Meta:
        model = mainenquiry
        fields = "__all__"

