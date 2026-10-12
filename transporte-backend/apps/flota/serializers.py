from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from apps.nucleo.constantes import MARGEN_VENTA_MINUTOS
from apps.nucleo.validadores import validar_dni

from .models import Conductor, Vehiculo, Viaje


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = "__all__"
        read_only_fields = ("creado_en", "actualizado_en")


class ConductorSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField()

    class Meta:
        model = Conductor
        fields = "__all__"
        read_only_fields = ("creado_en", "actualizado_en")

    def validate_dni(self, value):
        return validar_dni(value)


class ViajeListSerializer(serializers.ModelSerializer):
    ruta_descripcion = serializers.SerializerMethodField()
    vehiculo_placa = serializers.CharField(source="vehiculo.placa", read_only=True)
    conductor_nombre = serializers.CharField(
        source="conductor.nombre_completo", read_only=True
    )
    asientos_disponibles = serializers.SerializerMethodField()
    asientos_ocupados = serializers.SerializerMethodField()
    precio_base = serializers.DecimalField(
        source="ruta.precio_base", max_digits=8, decimal_places=2, read_only=True
    )
    capacidad = serializers.IntegerField(source="vehiculo.capacidad", read_only=True)
    acepta_venta = serializers.SerializerMethodField()

    class Meta:
        model = Viaje
        fields = (
            "id",
            "ruta",
            "ruta_descripcion",
            "vehiculo",
            "vehiculo_placa",
            "capacidad",
            "conductor",
            "conductor_nombre",
            "fecha_salida",
            "fecha_llegada",
            "estado",
            "precio_base",
            "asientos_disponibles",
            "asientos_ocupados",
            "acepta_venta",
            "creado_en",
            "activo",
        )
        read_only_fields = ("creado_en", "actualizado_en")

    def get_ruta_descripcion(self, obj):
        try:
            return f"{obj.ruta.origen.nombre} → {obj.ruta.destino.nombre}"
        except AttributeError:
            return str(obj.ruta)

    def get_asientos_ocupados(self, obj):
        try:
            from apps.pasajes.models import Pasaje

            return Pasaje.objects.filter(
                viaje=obj, estado__in=["emitido", "embarcado"]
            ).count()
        except Exception:
            return 0

    def get_asientos_disponibles(self, obj):
        try:
            return obj.vehiculo.capacidad - self.get_asientos_ocupados(obj)
        except Exception:
            return 0

    def get_acepta_venta(self, obj):
        """True si aún se pueden vender pasajes (hasta MARGEN_VENTA_MINUTOS tras la salida)."""
        ahora = timezone.now()
        limite = obj.fecha_salida + timedelta(minutes=MARGEN_VENTA_MINUTOS)
        return ahora <= limite and obj.estado not in [
            Viaje.Estado.COMPLETADO,
            Viaje.Estado.CANCELADO,
        ]


class ViajeDetalleSerializer(serializers.ModelSerializer):
    ruta_descripcion = serializers.SerializerMethodField()
    vehiculo_detalle = VehiculoSerializer(source="vehiculo", read_only=True)
    conductor_detalle = ConductorSerializer(source="conductor", read_only=True)
    asientos_disponibles = serializers.SerializerMethodField()
    asientos_ocupados = serializers.SerializerMethodField()
    precio_base = serializers.DecimalField(
        source="ruta.precio_base", max_digits=8, decimal_places=2, read_only=True
    )
    capacidad = serializers.IntegerField(source="vehiculo.capacidad", read_only=True)

    class Meta:
        model = Viaje
        fields = "__all__"
        read_only_fields = ("creado_en", "actualizado_en")

    def get_ruta_descripcion(self, obj):
        try:
            return f"{obj.ruta.origen.nombre} → {obj.ruta.destino.nombre}"
        except AttributeError:
            return str(obj.ruta)

    def get_asientos_ocupados(self, obj):
        try:
            from apps.pasajes.models import Pasaje

            return Pasaje.objects.filter(
                viaje=obj, estado__in=["emitido", "embarcado"]
            ).count()
        except Exception:
            return 0

    def get_asientos_disponibles(self, obj):
        try:
            return obj.vehiculo.capacidad - self.get_asientos_ocupados(obj)
        except Exception:
            return 0

    def validate(self, data):
        fecha_salida = data.get("fecha_salida")
        fecha_llegada = data.get("fecha_llegada")

        # Llegada posterior a salida
        if fecha_llegada and fecha_salida and fecha_llegada <= fecha_salida:
            raise serializers.ValidationError(
                "La fecha de llegada debe ser posterior a la fecha de salida."
            )

        # No programar viajes en el pasado (solo en creación)
        if not self.instance and fecha_salida and fecha_salida < timezone.now():
            raise serializers.ValidationError(
                "No se puede programar un viaje con fecha de salida en el pasado."
            )

        self._validar_disponibilidad(data)
        return data

    @staticmethod
    def _fin_estimado(salida, llegada, ruta):
        """Llegada registrada o, si no hay, salida + duración estimada de la ruta."""
        if llegada:
            return llegada
        return salida + timedelta(hours=float(ruta.duracion_horas or 0))

    def _validar_disponibilidad(self, data):
        """Un vehículo o conductor no puede estar en dos viajes que se solapen."""
        inst = self.instance
        salida = data.get("fecha_salida", inst.fecha_salida if inst else None)
        llegada = data.get("fecha_llegada", inst.fecha_llegada if inst else None)
        ruta = data.get("ruta", inst.ruta if inst else None)
        vehiculo = data.get("vehiculo", inst.vehiculo if inst else None)
        conductor = data.get("conductor", inst.conductor if inst else None)
        if not (salida and ruta and vehiculo and conductor):
            return

        fin = self._fin_estimado(salida, llegada, ruta)
        cercanos = (
            Viaje.objects.filter(
                activo=True,
                estado__in=[Viaje.Estado.PROGRAMADO, Viaje.Estado.EN_CURSO],
                fecha_salida__lt=fin,
                fecha_salida__gte=salida - timedelta(days=7),
            )
            .filter(Q(vehiculo=vehiculo) | Q(conductor=conductor))
            .select_related("ruta", "ruta__origen", "ruta__destino")
        )
        if inst:
            cercanos = cercanos.exclude(pk=inst.pk)

        errores = {}
        for otro in cercanos:
            otro_fin = self._fin_estimado(
                otro.fecha_salida, otro.fecha_llegada, otro.ruta
            )
            if otro_fin <= salida:
                continue
            hora = timezone.localtime(otro.fecha_salida).strftime("%d/%m/%Y %H:%M")
            detalle = f"ya está asignado al viaje {otro.ruta} del {hora}."
            if otro.vehiculo_id == vehiculo.id:
                errores["vehiculo"] = f"El vehículo {detalle}"
            if otro.conductor_id == conductor.id:
                errores["conductor"] = f"El conductor {detalle}"
        if errores:
            raise serializers.ValidationError(errores)
