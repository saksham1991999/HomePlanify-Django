from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import BusinessSerializer, CustomerSerializer, TaskSerializer, LabelSerializer, LabelCustomerSerializer
from .models import Customer, Business, Task, Note, Label


class BusinessAPIViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()
    permissions = [IsAuthenticated]


class CustomerAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permissions = [IsAuthenticated]


class LabelAPIViewSet(viewsets.ModelViewSet):
    serializer_class = LabelCustomerSerializer
    queryset = Label.objects.all()
    permissions = [IsAuthenticated]


