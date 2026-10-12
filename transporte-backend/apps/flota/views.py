from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.utils.dateparse import parse_date, parse_datetime
from django_filters.rest_framework import DjangoFilterBackend
from apps.nucleo.permisos import LecturaAutenticadoEscrituraGestion
from .models import Vehiculo, Conductor, Viaje
from .serializers import (
    VehiculoSerializer,
    ConductorSerializer,
    ViajeListSerializer,
    ViajeDetalleSerializer,
)


def _parsear(funcion, texto):
    """parse_date/parse_datetime lanzan ValueError con fechas imposibles (mes 13...)."""
    try:
        return funcion(texto)
    except ValueError:
        return None


class VehiculoViewSet(viewsets.ModelViewSet):
    permission_classes = [LecturaAutenticadoEscrituraGestion]
    queryset = Vehiculo.objects.filter(activo=True)
    serializer_class = VehiculoSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["estado"]
    search_fields = ["placa", "marca", "modelo"]
    ordering_fields = ["placa", "marca", "anio"]

    @action(detail=True, methods=["post"])
    def cambiar_estado(self, request, pk=None):
        vehiculo = self.get_object()
        estado = request.data.get("estado")
        if estado not in dict(Vehiculo.Estado.choices):
            return Response(
                {"error": "Estado no válido."}, status=status.HTTP_400_BAD_REQUEST
            )
        vehiculo.estado = estado
        vehiculo.save()
        return Response(
            {"mensaje": f"Estado actualizado a {vehiculo.get_estado_display()}"}
        )


class ConductorViewSet(viewsets.ModelViewSet):
    permission_classes = [LecturaAutenticadoEscrituraGestion]
    queryset = Conductor.objects.filter(activo=True)
    serializer_class = ConductorSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["estado", "categoria_licencia"]
    search_fields = ["dni", "nombres", "apellidos", "licencia"]
    ordering_fields = ["apellidos", "nombres"]

    @action(detail=True, methods=["post"])
    def cambiar_estado(self, request, pk=None):
        conductor = self.get_object()
        estado = request.data.get("estado")
        if estado not in dict(Conductor.Estado.choices):
            return Response(
                {"error": "Estado no válido."}, status=status.HTTP_400_BAD_REQUEST
            )
        conductor.estado = estado
        conductor.save()
        return Response(
            {"mensaje": f"Estado actualizado a {conductor.get_estado_display()}"}
        )


class ViajeViewSet(viewsets.ModelViewSet):
    permission_classes = [LecturaAutenticadoEscrituraGestion]
    queryset = Viaje.objects.select_related(
        "ruta", "ruta__origen", "ruta__destino", "vehiculo", "conductor"
    ).filter(activo=True)

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["estado", "ruta", "fecha_salida"]
    search_fields = ["vehiculo__placa", "conductor__apellidos", "ruta__origen__nombre"]
    ordering_fields = ["fecha_salida", "estado"]

    def get_serializer_class(self):
        if self.action == "list":
            return ViajeListSerializer
        return ViajeDetalleSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # fecha_salida >= valor dado (incluye hora). El "+" de la zona horaria
        # llega como espacio en la URL, por eso se reintenta reemplazándolo.
        fecha_salida__gte = self.request.query_params.get("fecha_salida__gte")
        if fecha_salida__gte:
            valor = _parsear(parse_datetime, fecha_salida__gte) or _parsear(
                parse_datetime, fecha_salida__gte.replace(" ", "+")
            )
            if valor is None:
                raise ValidationError(
                    {
                        "fecha_salida__gte": "Formato inválido. Usa AAAA-MM-DDTHH:MM:SS+00:00."
                    }
                )
            qs = qs.filter(fecha_salida__gte=valor)

        # Fecha exacta (para el módulo de pasajes)
        fecha_salida__date = self.request.query_params.get("fecha_salida__date")
        if fecha_salida__date:
            valor = _parsear(parse_date, fecha_salida__date)
            if valor is None:
                raise ValidationError(
                    {"fecha_salida__date": "Formato inválido. Usa AAAA-MM-DD."}
                )
            qs = qs.filter(fecha_salida__date=valor)

        return qs

    @action(detail=True, methods=["post"])
    def cambiar_estado(self, request, pk=None):
        viaje = self.get_object()
        estado = request.data.get("estado")
        if estado not in dict(Viaje.Estado.choices):
            return Response(
                {"error": "Estado no válido."}, status=status.HTTP_400_BAD_REQUEST
            )
        viaje.estado = estado
        viaje.save()
        return Response(
            {"mensaje": f"Estado actualizado a {viaje.get_estado_display()}"}
        )

    @action(detail=True, methods=["get"])
    def asientos(self, request, pk=None):
        viaje = self.get_object()
        capacidad = viaje.vehiculo.capacidad

        from apps.pasajes.models import Pasaje

        ocupados = set(
            Pasaje.objects.filter(
                viaje=viaje, estado__in=["emitido", "embarcado"]
            ).values_list("asiento", flat=True)
        )

        asientos = [
            {"numero": num, "ocupado": num in ocupados}
            for num in range(1, capacidad + 1)
        ]

        return Response(
            {
                "viaje_id": viaje.id,
                "capacidad": capacidad,
                "asientos": asientos,
            }
        )
