from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
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
        business = Business.objects.get(user=self.request.user)
        customers = Customer.objects.filter(business=business)

        if self.request.query_params.get('search', None):
            search = self.request.query_params.get('search', None)
            customers = customers.filter(Q(name__icontains=search) | Q(mobile__icontains=search) | Q(location__icontains=search))

        if self.request.query_params.get('sort', None):
            sort = self.request.query_params.get('sort', None)
            if sort=='nameasc':
                customers = customers.order_by('name')
            elif sort == 'namedsc':
                customers = customers.order_by('-name')
            elif sort == 'dateasc':
                customers = customers.order_by('created_at')
            elif sort == 'datedsc':
                customers = customers.order_by('-created_at')
        return customers

    @action(detail=True, methods=['post'])
    def update_customer_label(self, request, pk, *args, **kwargs):
        customer = self.get_object()
        labels = request.data['labels']
        labels = list(map(int, labels.strip().split(",")))
        print(labels)
        customer.labels.clear()
        for label in labels:
            customer.labels.add(label)
        customer.save()
        return Response("Done", status = status.HTTP_206_PARTIAL_CONTENT)

    @action(detail=True, methods=['get'])
    def pin(self, request, pk, *args, **kwargs):
        try:
            customer = self.get_object()
            customer.pinned = True
            customer.save()
            return Response("Done", status = status.HTTP_206_PARTIAL_CONTENT)
        except:
            return Response("Error", status = status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def unpin(self, request, pk, *args, **kwargs):
        try:
            customer = self.get_object()
            customer.pinned = False
            customer.save()
            return Response("Done", status = status.HTTP_206_PARTIAL_CONTENT)
        except:
            return Response("Error", status = status.HTTP_400_BAD_REQUEST)


class LabelAPIViewSet(viewsets.ModelViewSet):
    serializer_class = LabelCustomerSerializer
    queryset = Label.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.query_params.get('global', None):
            label = Label.objects.filter(business__isnull=True)
        else:
            label = Label.objects.filter(Q(business__user = self.request.user) | Q(business__isnull=True))

        if self.request.query_params.get('sort', None):
            sort = self.request.query_params.get('sort', None)
            if sort == 'nameasc':
                label = label.order_by('name')
            if sort == 'namedsc':
                label = label.order_by('-name')

        if self.request.query_params.get('search', None):
            search = self.request.query_params.get('search', None)
            label = label.filter(color__icontains=search)
        
        return label    
     

class TaskAPIViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsTaskBusinessOwner]

    def get_queryset(self):
        tasks = Task.objects.filter(customer__business__user=self.request.user)

        if self.request.query_params.get('search', None):
            search = self.request.query_params.get('search', None)
            tasks = tasks.filter(Q(task__icontains=search) | Q(importance__icontains=search) | Q(completed__icontains=search))
            
        if self.request.query_params.get('sort', None):
            sort = self.request.query_params.get('sort', None)
            if sort=='nameasc':
                tasks = tasks.order_by('name')
            elif sort == 'namedsc':
                tasks = tasks.order_by('-name')
            elif sort == 'dateasc':
                tasks = tasks.order_by('datetime')
            elif sort == 'datedsc':
                tasks = tasks.order_by('-datetime')

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
        
        if self.request.query_params.get('sort', None):
            sort = self.request.query_params.get('sort', None)
            if sort=='nameasc':
                notes = notes.order_by('name')
            elif sort == 'namedsc':
                notes = notes.order_by('-name')
        return notes
