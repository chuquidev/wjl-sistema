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
    EncomiendaCambiarEstadoSerializer,
    EncomiendaEntregarSerializer,
)


def _registrar_en_caja(encomienda, usuario):
    from apps.caja.models import SesionCaja, Transaccion

    # FIX: si no hay caja abierta, lanzar error y hacer rollback
    try:
        sesion = SesionCaja.objects.get(
            cajero=usuario,
            estado=SesionCaja.Estado.ABIERTA
        )
    except SesionCaja.DoesNotExist:
        raise ValidationError(
            'Debes tener una sesión de caja abierta para registrar encomiendas.'
        )

    Transaccion.objects.create(
        sesion                = sesion,
        tipo                  = Transaccion.Tipo.VENTA_ENCOMIENDA,
        monto                 = encomienda.precio,
        descripcion           = (
            f'Encomienda {str(encomienda.codigo)[:8].upper()} — '
            f'{encomienda.remitente_nombre} → {encomienda.destinatario_nombre}'
        ),
        referencia_encomienda = encomienda,
    )


class EncomiendaViewSet(viewsets.ModelViewSet):
    queryset = Encomienda.objects.select_related(
        'viaje', 'viaje__ruta', 'registrado_por', 'sucursal_origen'
    ).filter(activo=True)

    filter_backends   = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields  = ['estado', 'viaje', 'sucursal_origen']
    search_fields     = ['remitente_nombre', 'remitente_dni', 'destinatario_nombre', 'destinatario_dni', 'codigo']
    ordering_fields   = ['creado_en', 'precio']
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'create':
            return EncomiendaCrearSerializer
        return EncomiendaListSerializer

    # FIX: transaction.atomic — si _registrar_en_caja falla, la encomienda NO se guarda
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = EncomiendaCrearSerializer(
            data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        instancia = serializer.save()
        _registrar_en_caja(instancia, request.user)  # si falla → rollback

        return Response(
            EncomiendaListSerializer(instancia, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        encomienda = self.get_object()
        serializer = EncomiendaCambiarEstadoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nuevo = serializer.validated_data['estado']

        mapa = {
            'en_transito': Encomienda.Estado.EN_TRANSITO,
            'entregado':   Encomienda.Estado.ENTREGADA,
            'devuelto':    Encomienda.Estado.DEVUELTA,
        }
        flujo = {
            Encomienda.Estado.REGISTRADA:  [Encomienda.Estado.EN_TRANSITO, Encomienda.Estado.DEVUELTA],
            Encomienda.Estado.EN_TRANSITO: [Encomienda.Estado.ENTREGADA,   Encomienda.Estado.DEVUELTA],
        }

        estado_nuevo = mapa.get(nuevo)
        if estado_nuevo not in flujo.get(encomienda.estado, []):
            return Response(
                {'error': f'No se puede cambiar de "{encomienda.estado}" a "{nuevo}".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        encomienda.estado = estado_nuevo
        encomienda.save(update_fields=['estado', 'actualizado_en'])
        return Response(
            EncomiendaListSerializer(encomienda, context=self.get_serializer_context()).data
        )

    @action(detail=True, methods=['post'])
    def entregar(self, request, pk=None):
        encomienda = self.get_object()
        if encomienda.estado == Encomienda.Estado.ENTREGADA:
            return Response({'error': 'La encomienda ya fue entregada.'}, status=400)
        if encomienda.estado != Encomienda.Estado.EN_TRANSITO:
            return Response({'error': 'Solo se pueden entregar encomiendas en tránsito.'}, status=400)

        serializer = EncomiendaEntregarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        encomienda.estado        = Encomienda.Estado.ENTREGADA
        encomienda.entregado_a   = serializer.validated_data['entregado_a']
        encomienda.fecha_entrega = timezone.now()
        encomienda.save(update_fields=['estado', 'entregado_a', 'fecha_entrega', 'actualizado_en'])
        return Response(
            EncomiendaListSerializer(encomienda, context=self.get_serializer_context()).data
        )

    @action(detail=True, methods=['post'])
    def devolver(self, request, pk=None):
        encomienda = self.get_object()
        if encomienda.estado in [Encomienda.Estado.ENTREGADA, Encomienda.Estado.DEVUELTA]:
            return Response(
                {'error': f'No se puede devolver con estado "{encomienda.estado}".'},
                status=400
            )
        encomienda.estado = Encomienda.Estado.DEVUELTA
        encomienda.save(update_fields=['estado', 'actualizado_en'])
        return Response(
            EncomiendaListSerializer(encomienda, context=self.get_serializer_context()).data
        )

    @action(detail=False, methods=['get'])
    def rastrear(self, request):
        codigo = request.query_params.get('codigo', '').strip()
        if not codigo:
            return Response({'error': 'Proporciona el código de rastreo.'}, status=400)
        try:
            enc = Encomienda.objects.get(codigo__startswith=codigo.lower())
            return Response(EncomiendaListSerializer(enc, context=self.get_serializer_context()).data)
        except Encomienda.DoesNotExist:
            return Response({'error': 'No se encontró ninguna encomienda con ese código.'}, status=404)
        except Encomienda.MultipleObjectsReturned:
            return Response({'error': 'Código ambiguo, ingresa más caracteres.'}, status=400)