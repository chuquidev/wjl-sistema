from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.utils import timezone
from .models import Encomienda
from .serializers import (
    EncomiendaListSerializer,
    EncomiendaCrearSerializer,
    EncomiendaEntregarSerializer,
)
from rest_framework.pagination import PageNumberPagination


class EncomiendaPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


def _registrar_en_caja(encomienda, usuario):
    from apps.caja.models import SesionCaja, Transaccion

    try:
        sesion = SesionCaja.objects.get(
            cajero=usuario, estado=SesionCaja.Estado.ABIERTA
        )
    except SesionCaja.DoesNotExist:
        raise ValidationError(
            "Debes tener una sesión de caja abierta para registrar encomiendas."
        )

    Transaccion.objects.create(
        sesion=sesion,
        tipo=Transaccion.Tipo.VENTA_ENCOMIENDA,
        monto=encomienda.precio,
        descripcion=(
            f"Encomienda {str(encomienda.codigo)[:8].upper()} — "
            f"{encomienda.remitente_nombre} → {encomienda.destinatario_nombre}"
        ),
        referencia_encomienda=encomienda,
    )


class EncomiendaViewSet(viewsets.ModelViewSet):
    pagination_class = EncomiendaPagination
    queryset = Encomienda.objects.select_related(
        "viaje",
        "viaje__ruta",
        "viaje__ruta__origen",
        "viaje__ruta__destino",
        "viaje__vehiculo",
        "registrado_por",
        "sucursal_origen",
    ).filter(activo=True)

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["estado", "viaje", "sucursal_origen"]
    search_fields = [
        "remitente_nombre",
        "remitente_dni",
        "destinatario_nombre",
        "destinatario_dni",
        "codigo",
    ]
    ordering_fields = ["creado_en", "precio"]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.action == "create":
            return EncomiendaCrearSerializer
        return EncomiendaListSerializer

    # ── Crear ─────────────────────────────────────────────────
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = EncomiendaCrearSerializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        instancia = serializer.save()
        _registrar_en_caja(instancia, request.user)

        return Response(
            EncomiendaListSerializer(
                instancia, context=self.get_serializer_context()
            ).data,
            status=status.HTTP_201_CREATED,
        )

    # ── Actualizar (patch) ────────────────────────────────────
    def partial_update(self, request, *args, **kwargs):
        encomienda = self.get_object()
        if encomienda.estado == Encomienda.Estado.ENTREGADA:
            return Response(
                {"error": "No se puede modificar una encomienda ya entregada."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = EncomiendaListSerializer(
            encomienda,
            data=request.data,
            partial=True,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # ── Eliminar (soft delete) ────────────────────────────────
    def destroy(self, request, *args, **kwargs):
        encomienda = self.get_object()
        if encomienda.estado not in [Encomienda.Estado.REGISTRADA]:
            return Response(
                {"error": "Solo se pueden eliminar encomiendas en estado registrada."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        encomienda.activo = False
        encomienda.save(update_fields=["activo", "actualizado_en"])
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ── Viajes disponibles para el día seleccionado ───────────
    @action(detail=False, methods=["get"], url_path="viajes-disponibles")
    def viajes_disponibles(self, request):
        from apps.flota.models import Viaje
        from apps.flota.serializers import ViajeListSerializer

        fecha = request.query_params.get("fecha")
        if not fecha:
            return Response(
                {"error": "Proporciona el parámetro fecha (YYYY-MM-DD)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ahora = timezone.now()
        limite = ahora - timezone.timedelta(minutes=20)

        viajes = (
            Viaje.objects.filter(
                fecha_salida__date=fecha,
                estado=Viaje.Estado.PROGRAMADO,
                fecha_salida__gte=limite,
            )
            .select_related("ruta", "ruta__origen", "ruta__destino", "vehiculo")
            .order_by("fecha_salida")
        )

        serializer = ViajeListSerializer(
            viajes, many=True, context=self.get_serializer_context()
        )
        return Response(serializer.data)

    # ── Entregar ──────────────────────────────────────────────
    # Permite entregar desde cualquier estado activo (registrada o en_transito)
    @action(detail=True, methods=["post"])
    def entregar(self, request, pk=None):
        encomienda = self.get_object()

        if encomienda.estado == Encomienda.Estado.ENTREGADA:
            return Response({"error": "La encomienda ya fue entregada."}, status=400)
        if encomienda.estado == Encomienda.Estado.DEVUELTA:
            return Response(
                {"error": "No se puede entregar una encomienda devuelta."}, status=400
            )

        serializer = EncomiendaEntregarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        encomienda.estado = Encomienda.Estado.ENTREGADA
        encomienda.entregado_a = serializer.validated_data["entregado_a"]
        encomienda.fecha_entrega = timezone.now()
        encomienda.save(
            update_fields=["estado", "entregado_a", "fecha_entrega", "actualizado_en"]
        )
        return Response(
            EncomiendaListSerializer(
                encomienda, context=self.get_serializer_context()
            ).data
        )

    # ── Devolver ──────────────────────────────────────────────
    @action(detail=True, methods=["post"])
    def devolver(self, request, pk=None):
        encomienda = self.get_object()
        if encomienda.estado in [
            Encomienda.Estado.ENTREGADA,
            Encomienda.Estado.DEVUELTA,
        ]:
            return Response(
                {"error": f'No se puede devolver con estado "{encomienda.estado}".'},
                status=400,
            )
        encomienda.estado = Encomienda.Estado.DEVUELTA
        encomienda.save(update_fields=["estado", "actualizado_en"])
        return Response(
            EncomiendaListSerializer(
                encomienda, context=self.get_serializer_context()
            ).data
        )

    # ── Rastrear ──────────────────────────────────────────────
    @action(detail=False, methods=["get"])
    def rastrear(self, request):
        codigo = request.query_params.get("codigo", "").strip()
        if not codigo:
            return Response({"error": "Proporciona el código de rastreo."}, status=400)
        try:
            enc = Encomienda.objects.get(codigo__startswith=codigo.lower())
            return Response(
                EncomiendaListSerializer(
                    enc, context=self.get_serializer_context()
                ).data
            )
        except Encomienda.DoesNotExist:
            return Response(
                {"error": "No se encontró ninguna encomienda con ese código."},
                status=404,
            )
        except Encomienda.MultipleObjectsReturned:
            return Response(
                {"error": "Código ambiguo, ingresa más caracteres."}, status=400
            )
