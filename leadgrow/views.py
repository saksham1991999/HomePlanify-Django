from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q

from .serializers import BusinessSerializer, CustomerSerializer, TaskSerializer, LabelSerializer, LabelCustomerSerializer, NoteSerializer
from .models import Customer, Business, Task, Note, Label
from .permissions import IsBusinessOwner, IsCustomerBusinessOwner, IsTaskBusinessOwner, IsNoteBusinessOwner


class BusinessAPIViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()
    permission_classes = [IsAuthenticated, IsBusinessOwner]

    def get_queryset(self):
        business = Business.objects.filter(user=self.request.user)
        return business


class CustomerAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated, IsCustomerBusinessOwner]

    def get_queryset(self):
        business = Business.objects.filter(user=self.request.user)
        customers = Customer.objects.filter(business=business)

        if self.request.query_params.get('search', None):
            search = self.request.query_params.get('search', None)
            customers = customers.filter(Q(name__icontains=search) | Q(mobile__icontains=search) | Q(location__icontains=search))
        return customers


class LabelAPIViewSet(viewsets.ModelViewSet):
    serializer_class = LabelCustomerSerializer
    queryset = Label.objects.all()
    permission_classes = [IsAuthenticated]


class TaskAPIViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsTaskBusinessOwner]

    def get_queryset(self):
        tasks = Task.objects.filter(customer__business__user=self.request.user)

        if self.request.query_params.get('search', None):
            search = self.request.query_params.get('search', None)
            tasks = tasks.filter(Q(task__icontains=search) | Q(importance__icontains=search))
        return tasks


class NoteAPIViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated, IsNoteBusinessOwner]

    def get_queryset(self):
        notes = Note.objects.filter(customer__business__user=self.request.user)

        if self.request.query_params.get('search', None):
            search = self.request.query_params.get('search', None)
            notes = notes.filter(note__icontains=search)
        return notes
