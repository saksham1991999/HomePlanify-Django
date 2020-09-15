# from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import User, property, images, bookmark, contact, enquiry, mainenquiry


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = property
        fields = "__all__"

class ImagesSerializer(serializers.ModelSerializer):


    class Meta:
        model = images
        fields = "__all__"

class BookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = bookmark
        fields = "__all__"

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = contact
        fields = "__all__"

class EnquirySerializer(serializers.ModelSerializer):

    class Meta:
        model = enquiry
        fields = "__all__"

class MainEnquirySerializer(serializers.ModelSerializer):

    class Meta:
        model = mainenquiry
        fields = "__all__"

