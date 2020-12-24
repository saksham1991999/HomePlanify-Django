# from django.contrib.auth.models import User
from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import User, features, property, images, bookmark, contact, enquiry, mainenquiry, InvestProperties, FeaturedProperty


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

class CustomRegisterSerializer(RegisterSerializer):
    mobile = serializers.CharField(allow_blank = True, allow_null=True)
    first_name = serializers.CharField(allow_blank = True, allow_null=True)
    last_name = serializers.CharField(allow_blank = True, allow_null=True)
    email = serializers.EmailField(allow_blank = True, allow_null=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'mobile', 'first_name', 'last_name')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'mobile': self.validated_data.get('mobile', ''),

        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.mobile = self.cleaned_data.get('mobile')
        user.save()
        adapter.save_user(request, user, self)
        return user


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key', 'user')

class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = features
        fields = "__all__"

class InvestPropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestProperties
        fields = "__all__"

class FeaturedPropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = FeaturedProperty
        fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField(read_only = True)
    bookmarked = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = property
        fields = "__all__"

    def get_photos(self, obj):
        serializer_context = {'request': self.context.get('request')}
        photos = images.objects.filter(property = obj)
        data = ImagesSerializer(photos, many=True, context = serializer_context).data
        return data

    def get_bookmarked(self, obj):
        user = self.context['request'].user
        if user.id is not None:
            user_bookmarks = bookmark.objects.filter(user=user)
            if user_bookmarks:
                user_bookmarks = user_bookmarks[0]
                properties_bookmarked = user_bookmarks.properties.all()
                if obj in properties_bookmarked:
                    return True
            return False
        return None

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

