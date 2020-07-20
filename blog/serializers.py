# from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from . import models



class CategoriesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="category-detail")

    class Meta:
        model = models.categories
        fields = "__all__"

class BlogPostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="post-detail")

    class Meta:
        model = models.post
        fields = "__all__"

class BlogPostCommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="comment-detail")

    class Meta:
        model = models.comment
        fields = "__all__"