from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import SesionCaja, Transaccion
from apps.nucleo.permisos import es_administrador, es_supervisor
from .serializers import (
    SesionCajaListSerializer,
    SesionCajaAbrirSerializer,
    SesionCajaCerrarSerializer,
    TransaccionSerializer,
    GastoSerializer,
)


class SesionCajaViewSet(viewsets.ModelViewSet):
    queryset = SesionCaja.objects.select_related("cajero", "sucursal").all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["estado", "sucursal", "cajero"]
    ordering_fields = ["fecha_apertura"]
    http_method_names = ["get", "post", "head", "options"]

    def get_serializer_class(self):
        if self.action == "create":
            return SesionCajaAbrirSerializer
        return SesionCajaListSerializer

    def get_queryset(self):
        """Cada cajero solo ve sus propias sesiones (salvo admin)."""
        user = self.request.user
        qs = super().get_queryset()
        if es_administrador(user) or es_supervisor(user):
            return qs
        return qs.filter(cajero=user)

    def perform_create(self, serializer):
        serializer.save()

    # ── Cerrar caja ───────────────────────────────────────────
    @action(detail=True, methods=["post"])
    def cerrar(self, request, pk=None):
        sesion = self.get_object()

        if sesion.cajero != request.user and not request.user.is_staff:
            raise PermissionDenied("Solo puedes cerrar tu propia sesión de caja.")

        if sesion.estado == SesionCaja.Estado.CERRADA:
            return Response(
                {"error": "Esta sesión ya está cerrada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SesionCajaCerrarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sesion.monto_final = serializer.validated_data["monto_final"]
        sesion.observacion = serializer.validated_data.get("observacion", "")
        sesion.estado = SesionCaja.Estado.CERRADA
        sesion.fecha_cierre = timezone.now()
        sesion.save()

        diferencia = float(sesion.monto_final) - float(sesion.saldo_esperado)

        return Response(
            {
                "mensaje": "Caja cerrada correctamente.",
                "saldo_esperado": sesion.saldo_esperado,
                "monto_final": sesion.monto_final,
                "diferencia": round(diferencia, 2),
            }
        )

    # ── Registrar gasto ───────────────────────────────────────
    @action(detail=True, methods=["post"])
    def registrar_gasto(self, request, pk=None):
        sesion = self.get_object()

        if sesion.cajero != request.user and not request.user.is_staff:
            raise PermissionDenied(
                "No puedes registrar gastos en la caja de otro cajero."
            )

        if sesion.estado == SesionCaja.Estado.CERRADA:
            return Response(
                {"error": "No se puede registrar gastos en una caja cerrada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = GastoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Transaccion.objects.create(
            sesion=sesion,
            tipo=Transaccion.Tipo.GASTO,
            monto=serializer.validated_data["monto"],
            descripcion=serializer.validated_data["descripcion"],
        )

        return Response({"mensaje": "Gasto registrado correctamente."})

    # ── Mi sesión activa ──────────────────────────────────────
    @action(detail=False, methods=["get"])
    def mi_sesion(self, request):
        try:
            sesion = SesionCaja.objects.select_related("cajero", "sucursal").get(
                cajero=request.user, estado=SesionCaja.Estado.ABIERTA
            )
            serializer = SesionCajaListSerializer(sesion)
            return Response(serializer.data)
        except SesionCaja.DoesNotExist:
            return Response(
                {"mensaje": "No tienes una sesión de caja abierta."},
                status=status.HTTP_404_NOT_FOUND,
            )

    # ── Transacciones de una sesión ───────────────────────────
    @action(detail=True, methods=["get"])
    def transacciones(self, request, pk=None):
        sesion = self.get_object()
        transacciones = sesion.transacciones.all()
        serializer = TransaccionSerializer(transacciones, many=True)
        return Response(serializer.data)

    # ── Consolidado por sede (solo administradores) ───────────
    @action(detail=False, methods=["get"])
    def consolidado(self, request):
        from django.db.models import Sum, Count, Q
        from apps.ubicaciones.models import Sucursal

        if not (
            request.user.is_staff or getattr(request.user, "rol", "") == "administrador"
        ):
            return Response(
                {"error": "No tienes permiso para ver este resumen."},
                status=status.HTTP_403_FORBIDDEN,
            )

        fecha_desde = request.query_params.get("fecha_desde")
        fecha_hasta = request.query_params.get("fecha_hasta")

        sesiones_qs = SesionCaja.objects.select_related("sucursal", "cajero").all()
        if fecha_desde:
            sesiones_qs = sesiones_qs.filter(fecha_apertura__date__gte=fecha_desde)
        if fecha_hasta:
            sesiones_qs = sesiones_qs.filter(fecha_apertura__date__lte=fecha_hasta)

        sucursales = Sucursal.objects.all()
        resultado = []
        total_global = {
            "ingresos": 0,
            "egresos": 0,
            "anulaciones": 0,
            "cajas_abiertas": 0,
            "cajas_cerradas": 0,
            "total_sesiones": 0,
        }

        for sucursal in sucursales:
            ses = sesiones_qs.filter(sucursal=sucursal)
            t = ses.aggregate(
                ingresos=Sum(
                    "transacciones__monto",
                    filter=Q(
                        transacciones__tipo__in=["venta_pasaje", "venta_encomienda"]
                    ),
                ),
                egresos=Sum(
                    "transacciones__monto", filter=Q(transacciones__tipo="gasto")
                ),
                anulaciones=Sum(
                    "transacciones__monto", filter=Q(transacciones__tipo="anulacion")
                ),
                cajas_abiertas=Count("id", filter=Q(estado="abierta"), distinct=True),
                cajas_cerradas=Count("id", filter=Q(estado="cerrada"), distinct=True),
            )

            ingresos = float(t["ingresos"] or 0)
            egresos = float(t["egresos"] or 0)
            anulaciones = float(t["anulaciones"] or 0)
            abiertas = t["cajas_abiertas"] or 0
            cerradas = t["cajas_cerradas"] or 0

            activas = ses.filter(estado="abierta").values(
                "id",
                "cajero__nombres",
                "cajero__apellidos",
                "monto_inicial",
                "fecha_apertura",
            )

            resultado.append(
                {
                    "sucursal_id": sucursal.id,
                    "sucursal_nombre": sucursal.nombre,
                    "ingresos": round(ingresos, 2),
                    "egresos": round(egresos, 2),
                    "anulaciones": round(anulaciones, 2),
                    "saldo_neto": round(ingresos - egresos - anulaciones, 2),
                    "cajas_abiertas": abiertas,
                    "cajas_cerradas": cerradas,
                    "total_sesiones": abiertas + cerradas,
                    "sesiones_activas": [
                        {
                            "id": s["id"],
                            "cajero": f"{s['cajero__nombres']} {s['cajero__apellidos']}".strip(),
                            "monto_inicial": float(s["monto_inicial"] or 0),
                            "fecha_apertura": s["fecha_apertura"],
                        }
                        for s in activas
                    ],
                }
            )

            total_global["ingresos"] += ingresos
            total_global["egresos"] += egresos
            total_global["anulaciones"] += anulaciones
            total_global["cajas_abiertas"] += abiertas
            total_global["cajas_cerradas"] += cerradas
            total_global["total_sesiones"] += abiertas + cerradas

        return Response(
            {
                "sedes": resultado,
                "total_global": {
                    k: round(v, 2) if isinstance(v, float) else v
                    for k, v in total_global.items()
                },
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta,
            }
        )


class TransaccionViewSet(viewsets.ModelViewSet):
    """
    Transacciones son inmutables.
    PUT / PATCH / DELETE no permitidos.
    """

    queryset = Transaccion.objects.select_related(
        "sesion", "sesion__cajero", "sesion__sucursal"
    ).all()
    serializer_class = TransaccionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["tipo", "sesion"]
    ordering_fields = ["creado_en", "monto"]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        """Cajero solo ve movimientos de sus propias sesiones."""
        user = self.request.user
        qs = super().get_queryset()
        if es_administrador(user) or es_supervisor(user):
            return qs
        return qs.filter(sesion__cajero=user)


    def perform_create(self, serializer):
        sesion = serializer.validated_data.get("sesion")

        # Manualmente solo se registran GASTOS. Las ventas y anulaciones las
        # genera el sistema al vender/anular pasajes y encomiendas.
        if serializer.validated_data.get("tipo") != Transaccion.Tipo.GASTO:
            raise ValidationError(
                {
                    "tipo": "Solo se pueden registrar gastos manualmente. "
                    "Las ventas y anulaciones las genera el sistema."
                }
            )

        if sesion.estado == SesionCaja.Estado.CERRADA:
            raise ValidationError(
                "No se pueden registrar movimientos en una sesión cerrada."
            )
        if sesion.cajero != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied(
                "Solo puedes registrar movimientos en tu propia caja."
            )

        # Un gasto manual nunca se asocia a un pasaje o encomienda.
        serializer.save(referencia_pasaje=None, referencia_encomienda=None)
