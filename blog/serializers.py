# from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from . import models



class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.categories
        fields = "__all__"

class BlogPostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = models.post
        fields = "__all__"

    def get_comments(self, obj):
        comments = models.comment.objects.filter(post = obj)
        data = BlogPostCommentSerializer(comments, many=True).data
        return data


class BlogPostCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.comment
        fields = "__all__"