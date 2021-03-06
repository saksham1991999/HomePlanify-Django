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
from .permissions import IsOwnerOrReadOnly, ReadOnly

"""
Model View Set

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
"""
class UserAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class FeaturesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FeaturesSerializer
    queryset = models.features.objects.all()
    permissions = [ReadOnly]


class InvestPropertiesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InvestPropertySerializer
    queryset = models.InvestProperties.objects.all()
    permissions = [ReadOnly]

class FeaturedPropertiesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FeaturedPropertySerializer
    queryset = models.FeaturedProperty.objects.all()
    permissions = [ReadOnly]

class PropertiesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PropertySerializer
    # queryset = UserProfile.objects.all()

    def get_queryset(self):
        properties =  models.property.objects.filter()

        if self.request.query_params.get('visible', None):
            properties = properties.filter(visible=True)

        if self.request.query_params.get('verified', None):
            properties = properties.filter(verified=True)

        if self.request.query_params.get('search', None):
            search = self.request.query_params.get('search', None)
            properties = properties.filter(Q(property_name__icontains=search) | Q(additional_features__icontains = search) | Q(city__icontains=search))

        if self.request.query_params.get('type', None):
            type = self.request.query_params.get('type', None)
            properties = properties.filter(type=type)

        if self.request.query_params.get('bedrooms', None):
            bedrooms = self.request.query_params.get('bedrooms', None)
            if int(bedrooms) > 4:
                properties = properties.filter(bedrooms__gte = int(bedrooms))
            elif int(bedrooms ) > 0:
                properties = properties.filter(bedrooms=int(bedrooms))

        if self.request.query_params.get('rooms', None):
            rooms = self.request.query_params.get('rooms', None)
            if int(rooms) > 4:
                properties = properties.filter(rooms__gte = int(rooms))
            elif int(rooms) > 0:
                properties = properties.filter(rooms=int(rooms))

        if self.request.query_params.get('bathrooms', None):
            bathrooms = self.request.query_params.get('bathrooms', None)
            if int(bathrooms) > 3:
                properties = properties.filter(bathrooms__gte = int(bathrooms))
            elif int(bathrooms) > 0:
                properties = properties.filter(bathrooms=int(bathrooms))

        if self.request.query_params.get('construction_status', None):
            construction_status = self.request.query_params.get('construction_status', None)
            properties = properties.filter(construction_status__icontains=construction_status)

        if self.request.query_params.get('price_start', None):
            price_start = self.request.query_params.get('price_start', None)
            properties = properties.filter(total_price__gte = price_start)

        if self.request.query_params.get('price_end', None):
            price_end = self.request.query_params.get('price_end', None)
            properties = properties.filter(total_price__lte=price_end)

        if self.request.query_params.get('minbhk', None):
            minbhk = self.request.query_params.get('minbhk', None)
            properties = properties.filter(bedrooms__gte = minbhk)

        if self.request.query_params.get('maxbhk', None):
            maxbhk = self.request.query_params.get('maxbhk', None)
            properties = properties.filter(bedrooms__lte=maxbhk)

        if self.request.query_params.get('city', None):
            city = self.request.query_params.get('city', None)
            properties = properties.filter( city__icontains = city)

        if self.request.query_params.get('place', None):
            place = self.request.query_params.get('place', None)
            properties = properties.filter(additional_features__ic=place)

        if self.request.query_params.get('userid', None):
            userid = self.request.query_params.get('userid', None)
            properties = properties.filter(owner__id=userid)

        if self.request.query_params.get('featured', None):
            properties = properties.filter(featured=True)

        if self.request.query_params.get('orderby', None):
            orderby = self.request.query_params.get('orderby', None)
            if orderby == 'price':
                properties = properties.order_by('total_price')
            elif orderby == 'bhk':
                properties = properties.order_by('bedrooms')
            elif orderby == 'views':
                properties = properties.order_by('-views')
            elif orderby == 'date':
                properties = properties.order_by('-dateadded')

        return properties

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        try:
            features = request.data['features']
            if "#" in features:
                features = features.strip()
                features = features.strip("#")
                features_list = features.split("#")
                request.data.pop('features')
                features_list = features.split("#")
                for feature in features_list:
                    request.data.update({'features':feature})
        except:
            pass
        # request.data['branches'] =  ast.literal_eval(request.data['branches'])
        serializer = self.get_serializer(data=request.data, context = serializer_context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_properties(self, request, pk=None):
        serializer_context = {
            'request': request,
        }
        user = request.user
        if request.auth or user:
            queryset = models.property.objects.filter(owner = user)
            serializer = serializers.PropertySerializer(queryset, many=True, context=serializer_context)
            return Response(serializer.data)
        else:
            return Response({"Status": "Please Log-in"})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def bookmarks(self, request, pk=None):
        serializer_context = {
            'request': request,
        }
        user = self.request.user
        bookmark = models.bookmark.objects.filter(user=user)
        if bookmark.exists():
            queryset = bookmark[0].properties.all()
            serializer = serializers.PropertySerializer(queryset, many=True, context = serializer_context)
            return Response(serializer.data)
        else:
            return Response({"Status": "No Property Bookmarked"})

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def add_to_bookmarks(self, request, pk=None):
        serializer_context = {
            'request': request,
        }
        property = self.get_object()
        user = self.request.user
        bookmark = models.bookmark.objects.filter(user=user)
        if bookmark.exists():
            bookmark = bookmark[0]
            bookmark.properties.add(property)
            bookmark.save()
            queryset = bookmark.properties.all()
            serializer = serializers.PropertySerializer(queryset, many=True, context = serializer_context)
            return Response(serializer.data)
        else:
            bookmark = models.bookmark.objects.create(user=request.user)
            bookmark.properties.add(property)
            queryset = bookmark.properties.all()
            serializer = serializers.PropertySerializer(queryset, many=True, context=serializer_context)
            return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def remove_from_bookmarks(self, request, pk=None):
        serializer_context = {
            'request': request,
        }
        property = self.get_object()
        user = self.request.user
        bookmark = models.bookmark.objects.filter(user=user)
        if bookmark.exists():
            bookmark = bookmark[0]
            bookmark.properties.remove(property)
            bookmark.save()
            queryset = bookmark.properties.all()
            serializer = serializers.PropertySerializer(queryset, many=True, context=serializer_context)
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
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
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
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class MainEnquiryAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MainEnquirySerializer
    queryset = models.mainenquiry.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]




