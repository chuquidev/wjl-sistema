from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.nucleo.permisos import LecturaAutenticadoEscrituraAdmin
from .models import Sucursal, Ciudad, Ruta, Parada
from .serializers import (
    SucursalSerializer,
    CiudadSerializer,
    RutaSerializer,
    ParadaSerializer,
)


class SucursalViewSet(viewsets.ModelViewSet):
    permission_classes = [LecturaAutenticadoEscrituraAdmin]
    queryset = Sucursal.objects.filter(activo=True)
    serializer_class = SucursalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nombre", "ciudad"]


class CiudadViewSet(viewsets.ModelViewSet):
    permission_classes = [LecturaAutenticadoEscrituraAdmin]
    queryset = Ciudad.objects.filter(activo=True)
    serializer_class = CiudadSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "departamento"]
    ordering_fields = ["nombre"]


class RutaViewSet(viewsets.ModelViewSet):
    permission_classes = [LecturaAutenticadoEscrituraAdmin]
    queryset = (
        Ruta.objects.select_related("origen", "destino")
        .prefetch_related("paradas")
        .filter(activo=True)
    )
    serializer_class = RutaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["origen", "destino"]
    search_fields = ["origen__nombre", "destino__nombre"]


class ParadaViewSet(viewsets.ModelViewSet):
    permission_classes = [LecturaAutenticadoEscrituraAdmin]
    queryset = Parada.objects.select_related("ruta", "ciudad").filter(activo=True)
    serializer_class = ParadaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["ruta"]
