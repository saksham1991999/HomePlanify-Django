from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q

from .serializers import ZoneSerializer, FirmSerializer
from .models import Zone, Firm
from .permissions import IsFirmOwner, IsAdminOrReadOnly


class ZoneAPIViewSet(viewsets.ModelViewSet):
    serializer_class = ZoneSerializer
    queryset = Zone.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class FirmAPIViewSet(viewsets.ModelViewSet):
    serializer_class = FirmSerializer
    queryset = Firm.objects.all()
    permission_classes = [IsFirmOwner]

    def get_queryset(self):
        firms = Firm.objects.all()

        if self.request.query_params.get('zone', None):
            zone = self.request.query_params.get('zone', None)
            firms = firms.filter(zone = zone)

        if self.request.query_params.get('user', None):
            firms = Firm.objects.filter(user=self.request.user)
        return firms
