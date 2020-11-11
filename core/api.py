from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly,BasePermission, SAFE_METHODS
from . import serializers
from . import models, forms
from blog import models as blogmodels
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
########## API VIEWS ###########

class UserAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class FeaturesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FeaturesSerializer
    queryset = models.features.objects.all()
    permissions = [ReadOnly]


class InvestPropertiesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InvestPropertySerializer
    queryset = models.InvestProperties.objects.all()

class FeaturedPropertiesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FeaturedPropertySerializer
    queryset = models.FeaturedProperty.objects.all()

class PropertiesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PropertySerializer
    # queryset = UserProfile.objects.all()

    def get_queryset(self):
        properties =  models.property.objects.filter(visible=True, verified=True)

        if self.request.query_params.get('minprice', None):
            minprice = self.request.query_params.get('minprice', None)
            properties = properties.filter(total_price__gte = minprice)

        if self.request.query_params.get('maxprice', None):
            maxprice = self.request.query_params.get('maxprice', None)
            properties = properties.filter(total_price__lte=maxprice)

        if self.request.query_params.get('minbhk', None):
            minbhk = self.request.query_params.get('minbhk', None)
            properties = properties.filter(bedrooms__gte = minbhk)

        if self.request.query_params.get('maxbhk', None):
            maxbhk = self.request.query_params.get('maxbhk', None)
            properties = properties.filter(bedrooms__lte=maxbhk)

        if self.request.query_params.get('city', None):
            city = self.request.query_params.get('city', None)
            properties = properties.filter( city__icontains = city)

        if self.request.query_params.get('type', None):
            type = self.request.query_params.get('type', None)
            properties = properties.filter(type=type)

        if self.request.query_params.get('place', None):
            place = self.request.query_params.get('place', None)
            properties = properties.filter(additional_features__ic=place)

        if self.request.query_params.get('userid', None):
            userid = self.request.query_params.get('userid', None)
            properties = properties.filter(owner__id=userid)

        if self.request.query_params.get('orderby', None):
            orderby = self.request.query_params.get('orderby', None)
            if orderby == 'price':
                properties = properties.order_by('total_price')
            elif orderby == 'bhk':
                properties = properties.order_by('bedrooms')
            elif orderby == 'views':
                properties = properties.order_by('-views')

        return properties

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_properties(self, request, pk=None):
        user = request.user
        if request.auth or user:
            queryset = models.property.objects.filter(owner = user)
            serializer = serializers.PropertySerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"Status": "Please Log-in"})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def bookmarks(self, request, pk=None):
        user = self.request.user
        bookmark = models.bookmark.objects.filter(user=user)
        if bookmark.exists():
            queryset = bookmark[0].properties.all()
            serializer = serializers.PropertySerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"Status": "No Property Bookmarked"})


    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def add_to_bookmarks(self, request, pk=None):
        property = self.get_object()
        user = self.request.user
        bookmark = models.bookmark.objects.filter(user=user)
        if bookmark.exists():
            bookmark = bookmark[0]
            bookmark.properties.add(property)
            bookmark.save()
            queryset = bookmark.properties.all()
            serializer = serializers.PropertySerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            bookmark = models.bookmark.objects.create(user=request.user)
            bookmark.properties.add(property)
            return Response({"Status": "Successfully Bookmarked"})


    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def remove_from_bookmarks(self, request, pk=None):
        property = self.get_object()
        user = self.request.user
        bookmark = models.bookmark.objects.filter(user=user)
        if bookmark.exists():
            bookmark = bookmark[0]
            bookmark.properties.remove(property)
            bookmark.save()
            queryset = bookmark.properties.all()
            serializer = serializers.PropertySerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"Status": "Bookmarks is Empty"})


class ImagesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ImagesSerializer
    queryset = models.images.objects.all()

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class BookmarkAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookmarkSerializer
    # queryset = UserProfile.objects.all()

    def get_queryset(self):
        try:
            userid = self.request.query_params.get('userid', None)
            bookmarks = models.bookmark.objects.filter(owner__id=userid)
        except:
            bookmarks = models.bookmark.objects.all()
        return bookmarks

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class ContactsAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ContactSerializer
    queryset = models.contact.objects.all()

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class EnquiryAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EnquirySerializer
    # queryset = UserProfile.objects.all()

    def get_queryset(self):
        try:
            id = self.request.query_params.get('propertyid', None)
            enquiries = models.enquiry.objects.filter(property__id=id)
        except:
            enquiries = models.enquiry.objects.all()
        return enquiries

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class MainEnquiryAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MainEnquirySerializer
    queryset = models.mainenquiry.objects.all()

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]




