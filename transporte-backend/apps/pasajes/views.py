import requests
from django.conf import settings
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction, IntegrityError
from .models import Pasajero, Pasaje
from .serializers import (
    PasajeroSerializer,
    PasajeListSerializer,
    PasajeCrearSerializer,
    PasajeAnularSerializer,
)


class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = Pasajero.objects.filter(activo=True)
    serializer_class = PasajeroSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["dni"]
    search_fields = ["nombres", "apellidos"]
    ordering_fields = ["apellidos", "nombres"]

    @action(detail=False, methods=["get"], url_path="consultar-dni")
    def consultar_dni(self, request):
        dni = request.query_params.get("dni", "").strip()

        if not dni or len(dni) != 8:
            return Response(
                {"error": "DNI inválido"}, status=status.HTTP_400_BAD_REQUEST
            )

        # ── 1. Buscar en BD propia primero ────────────────────────
        try:
            pasajero = Pasajero.objects.get(dni=dni)
            return Response(
                {
                    "id": pasajero.id,
                    "dni": pasajero.dni,
                    "nombres": pasajero.nombres,
                    "apellidos": pasajero.apellidos,
                    "telefono": pasajero.telefono,
                    "fuente": "local",
                }
            )
        except Pasajero.DoesNotExist:
            pass

        # ── 2. Consultar Decolecta si no está en BD ───────────────
        api_key = getattr(settings, "DECOLECTA_API_KEY", "")
        if api_key:
            try:
                resp = requests.get(
                    "https://api.decolecta.com/v1/reniec/dni",
                    params={"numero": dni},
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    timeout=5,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    nombres = data.get("first_name", "")
                    apellidos = f"{data.get('first_last_name', '')} {data.get('second_last_name', '')}".strip()
                    return Response(
                        {
                            "id": None,
                            "dni": dni,
                            "nombres": nombres,
                            "apellidos": apellidos,
                            "telefono": "",
                            "fuente": "decolecta",
                        }
                    )
            except Exception:
                pass

        # ── 3. No encontrado en ninguna fuente ────────────────────
        return Response([], status=status.HTTP_200_OK)


class PasajeViewSet(viewsets.ModelViewSet):
    queryset = Pasaje.objects.select_related(
        "viaje",
        "viaje__ruta",
        "viaje__ruta__origen",
        "viaje__ruta__destino",
        "pasajero",
        "vendido_por",
        "sucursal",
    ).filter(activo=True)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["estado", "viaje", "sucursal"]
    search_fields = ["pasajero__dni", "pasajero__apellidos", "codigo"]
    ordering_fields = ["creado_en", "precio"]
    http_method_names = ["get", "post", "head", "options"]

    def get_serializer_class(self):
        if self.action == "create":
            return PasajeCrearSerializer
        return PasajeListSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = PasajeCrearSerializer(
                data=request.data, context=self.get_serializer_context()
            )
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # ✅ Recargar desde BD con select_related para tener todos los campos
            from apps.pasajes.models import Pasaje

            pasaje = Pasaje.objects.select_related(
                "vendido_por",
                "sucursal",
                "viaje",
                "viaje__ruta",
                "viaje__ruta__origen",
                "viaje__ruta__destino",
                "pasajero",
            ).get(pk=serializer.instance.pk)

            return Response(
                PasajeListSerializer(
                    pasaje, context=self.get_serializer_context()
                ).data,
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError as e:
            # Solo traducimos el error de asiento duplicado; cualquier otro error
            # de integridad se propaga para no ocultarlo con un mensaje engañoso.
            if "pasaje_asiento_unico_activo" in str(e):
                return Response(
                    {
                        "asiento": [
                            "Este asiento ya ha sido reservado por otro usuario."
                        ]
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            raise

    def perform_create(self, serializer):
        from apps.caja.models import SesionCaja, Transaccion

        viaje = serializer.validated_data.get("viaje")
        precio = serializer.validated_data.get("precio") or viaje.ruta.precio_base

        # ── Verificar caja abierta ────────────────────────────────
        try:
            sesion = SesionCaja.objects.get(
                cajero=self.request.user,
                estado=SesionCaja.Estado.ABIERTA,
            )
        except SesionCaja.DoesNotExist:
            raise ValidationError(
                "Debes tener una sesión de caja abierta para vender pasajes."
            )

        # ── Determinar sucursal ───────────────────────────────────
        sucursal = self.request.user.sucursal or sesion.sucursal
        if not sucursal:
            raise ValidationError(
                "No se puede determinar la sucursal. "
                "Asigna una sucursal a tu usuario o abre caja en una sucursal."
            )

        pasaje = serializer.save(
            vendido_por=self.request.user,
            sucursal=sucursal,
            precio=precio,
        )

        # ── Transacción del pasaje ────────────────────────────────
        Transaccion.objects.create(
            sesion=sesion,
            tipo=Transaccion.Tipo.VENTA_PASAJE,
            monto=precio,
            descripcion=f"Venta pasaje - Asiento {pasaje.asiento} - {viaje.ruta}",
            referencia_pasaje=pasaje,
        )

        # ── Transacción por paquetes si los hay ───────────────────
        total_paquetes = pasaje.total_paquetes
        if total_paquetes > 0:
            Transaccion.objects.create(
                sesion=sesion,
                tipo=Transaccion.Tipo.VENTA_PASAJE,
                monto=total_paquetes,
                descripcion=(
                    f"Paquetes pasajero asiento {pasaje.asiento} - "
                    f"{pasaje.pasajero.nombre_completo} "
                    f"({pasaje.paquetes.count()} bulto(s))"
                ),
                referencia_pasaje=pasaje,
            )

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def anular(self, request, pk=None):
        from apps.caja.models import SesionCaja, Transaccion

        pasaje = self.get_object()

        if pasaje.estado == Pasaje.Estado.ANULADO:
            return Response(
                {"error": "El pasaje ya está anulado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if pasaje.estado == Pasaje.Estado.EMBARCADO:
            return Response(
                {"error": "No se puede anular un pasaje ya embarcado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PasajeAnularSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pasaje.estado = Pasaje.Estado.ANULADO
        pasaje.motivo_anulacion = serializer.validated_data["motivo"]
        pasaje.activo = False
        pasaje.save()

        # ── Anular todos los bultos del pasaje ────────────────────
        total_paquetes_anulados = pasaje.total_paquetes
        cantidad_bultos = pasaje.paquetes.filter(activo=True).count()
        pasaje.paquetes.filter(activo=True).update(activo=False)

        # ── Registrar en caja si hay sesión abierta ───────────────
        try:
            sesion = SesionCaja.objects.get(
                cajero=request.user,
                estado=SesionCaja.Estado.ABIERTA,
            )
            motivo_corto = serializer.validated_data["motivo"][:50]

            Transaccion.objects.create(
                sesion=sesion,
                tipo=Transaccion.Tipo.ANULACION,
                monto=pasaje.precio,
                descripcion=(
                    f"Anulación pasaje - Asiento {pasaje.asiento} - {motivo_corto}"
                ),
                referencia_pasaje=pasaje,
            )

            if total_paquetes_anulados > 0:
                Transaccion.objects.create(
                    sesion=sesion,
                    tipo=Transaccion.Tipo.ANULACION,
                    monto=total_paquetes_anulados,
                    descripcion=(
                        f"Anulación bultos pasaje asiento {pasaje.asiento} - "
                        f"{cantidad_bultos} bulto(s) - {motivo_corto}"
                    ),
                    referencia_pasaje=pasaje,
                )

        except SesionCaja.DoesNotExist:
            pass

        return Response({"mensaje": "Pasaje y bultos anulados correctamente."})

    @action(detail=True, methods=["post"])
    def embarcar(self, request, pk=None):
        pasaje = self.get_object()
        if pasaje.estado != Pasaje.Estado.EMITIDO:
            return Response(
                {"error": "Solo se pueden embarcar pasajes en estado emitido."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        pasaje.estado = Pasaje.Estado.EMBARCADO
        pasaje.save()
        return Response({"mensaje": "Pasajero embarcado correctamente."})

    @action(detail=False, methods=["get"])
    def por_viaje(self, request):
        viaje_id = request.query_params.get("viaje_id")
        if not viaje_id:
            return Response(
                {"error": "Debe proporcionar viaje_id."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # ✅ Emitidos + Embarcados
        pasajes = self.queryset.filter(
            viaje_id=viaje_id, estado__in=["emitido", "embarcado"]
        )
        serializer = PasajeListSerializer(pasajes, many=True)
        return Response(serializer.data)
