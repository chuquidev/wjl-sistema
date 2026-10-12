from decimal import Decimal

from rest_framework import serializers
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Pasajero, Pasaje, PaquetePasaje
from apps.flota.models import Viaje
from apps.nucleo.validadores import validar_dni
from apps.nucleo.permisos import es_administrador, es_supervisor
from apps.nucleo.constantes import MARGEN_VENTA_MINUTOS


class PasajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasajero
        fields = "__all__"
        read_only_fields = ("creado_en", "actualizado_en")

    def validate_dni(self, value):
        return validar_dni(value)


class PaquetePasajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaquetePasaje
        fields = ("id", "descripcion", "cantidad_bultos", "peso_kg", "precio_adicional")

    def validate_precio_adicional(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value

    def validate_cantidad_bultos(self, value):
        if value < 1:
            raise serializers.ValidationError("Debe ser al menos 1 bulto.")
        return value


class PasajeListSerializer(serializers.ModelSerializer):
    pasajero_nombre = serializers.SerializerMethodField()
    pasajero_dni = serializers.CharField(source="pasajero.dni", read_only=True)
    pasajero_telefono = serializers.CharField(
        source="pasajero.telefono", read_only=True
    )
    ruta_descripcion = serializers.SerializerMethodField()
    vehiculo_placa = serializers.CharField(
        source="viaje.vehiculo.placa", read_only=True
    )
    fecha_salida = serializers.DateTimeField(
        source="viaje.fecha_salida", read_only=True
    )
    paquetes = PaquetePasajeSerializer(many=True, read_only=True)
    total_paquetes = serializers.ReadOnlyField()
    tiene_paquetes = serializers.ReadOnlyField()

    vendido_por_nombre = serializers.SerializerMethodField()

    sucursal_nombre = serializers.CharField(source="sucursal.nombre", read_only=True)

    class Meta:
        model = Pasaje
        fields = (
            "id",
            "codigo",
            "pasajero",
            "pasajero_nombre",
            "pasajero_dni",
            "pasajero_telefono",
            "viaje",
            "ruta_descripcion",
            "vehiculo_placa",
            "fecha_salida",
            "asiento",
            "precio",
            "metodo_pago",
            "estado",
            "motivo_anulacion",
            "vendido_por",
            "sucursal",
            "paquetes",
            "total_paquetes",
            "tiene_paquetes",
            "vendido_por",
            "vendido_por_nombre",  # ← agregar vendido_por_nombre
            "sucursal",
            "sucursal_nombre",
            "creado_en",
        )
        read_only_fields = ("codigo", "creado_en")

    def get_pasajero_nombre(self, obj):
        return f"{obj.pasajero.nombres} {obj.pasajero.apellidos}"

    def get_ruta_descripcion(self, obj):
        try:
            return f"{obj.viaje.ruta.origen.nombre} → {obj.viaje.ruta.destino.nombre}"
        except AttributeError:
            return str(obj.viaje.ruta)

    def get_vendido_por_nombre(self, obj):
        if not obj.vendido_por:
            return ""
        nombres = obj.vendido_por.nombres or ""
        apellidos = obj.vendido_por.apellidos or ""
        # Primera palabra del nombre + primera inicial del apellido
        primer_nombre = nombres.split()[0] if nombres else ""
        primer_apellido = apellidos[0].upper() + "." if apellidos else ""
        return f"{primer_nombre} {primer_apellido}".strip()


class PasajeCrearSerializer(serializers.ModelSerializer):
    # Paquetes opcionales — lista vacía por defecto
    paquetes = PaquetePasajeSerializer(many=True, required=False, default=list)

    class Meta:
        model = Pasaje
        # sucursal NO está aquí — el backend la asigna en perform_create
        fields = (
            "id",
            "codigo",
            "viaje",
            "pasajero",
            "asiento",
            "precio",
            "metodo_pago",
            "paquetes",
        )
        read_only_fields = ("id", "codigo")

    def validate_precio(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        return value

    def _validar_descuento(self, viaje, precio):
        """
        El cajero puede dar descuento sobre el precio base de la ruta, pero solo
        hasta DESCUENTO_MAX_CAJERO_PORCENTAJE (settings, por defecto 20 %).
        Administrador y supervisor no tienen límite.
        """
        request = self.context.get("request")
        usuario = getattr(request, "user", None)
        if es_administrador(usuario) or es_supervisor(usuario):
            return

        porcentaje = getattr(settings, "DESCUENTO_MAX_CAJERO_PORCENTAJE", 20)
        base = viaje.ruta.precio_base
        minimo = (base * (Decimal(100) - Decimal(porcentaje)) / Decimal(100)).quantize(
            Decimal("0.01")
        )
        if precio < minimo:
            raise serializers.ValidationError(
                {
                    "precio": (
                        f"Un cajero puede dar como máximo {porcentaje}% de descuento. "
                        f"Precio mínimo para esta ruta: S/. {minimo}. "
                        f"Para un descuento mayor, solicita autorización a un supervisor."
                    )
                }
            )

    def validate(self, data):
        viaje = data.get("viaje")
        asiento = data.get("asiento")
        ahora = timezone.now()

        # ── Descuento máximo permitido al cajero ──────────────────
        self._validar_descuento(viaje, data["precio"])

        # ── Estado del viaje ──────────────────────────────────────
        if viaje.estado == Viaje.Estado.CANCELADO:
            raise serializers.ValidationError(
                "No se pueden vender pasajes: el viaje está cancelado."
            )
        if viaje.estado == Viaje.Estado.COMPLETADO:
            raise serializers.ValidationError(
                "No se pueden vender pasajes: el viaje ya fue completado."
            )

        # ── Límite de tiempo después de la salida ─────────────────
        limite = viaje.fecha_salida + timedelta(minutes=MARGEN_VENTA_MINUTOS)
        if ahora > limite:
            minutos = int((ahora - viaje.fecha_salida).total_seconds() / 60)
            raise serializers.ValidationError(
                f"No se pueden vender pasajes: el viaje salió hace {minutos} minutos "
                f"(límite: {MARGEN_VENTA_MINUTOS} minutos después de la salida)."
            )

        # ── Validar asiento dentro del rango ─────────────────────
        capacidad = viaje.vehiculo.capacidad
        if not asiento or asiento < 1 or asiento > capacidad:
            raise serializers.ValidationError(
                f"El asiento debe estar entre 1 y {capacidad}."
            )

        # ── Asiento ya ocupado ────────────────────────────────────
        if Pasaje.objects.filter(
            viaje=viaje,
            asiento=asiento,
            estado__in=[Pasaje.Estado.EMITIDO, Pasaje.Estado.EMBARCADO],
        ).exists():
            raise serializers.ValidationError(
                f"El asiento {asiento} ya está ocupado en este viaje."
            )

        # ── Pasajero duplicado en el mismo viaje ──────────────────
        pasajero = data.get("pasajero")
        if (
            pasajero
            and Pasaje.objects.filter(
                viaje=viaje,
                pasajero=pasajero,
                estado__in=[Pasaje.Estado.EMITIDO, Pasaje.Estado.EMBARCADO],
            ).exists()
        ):
            raise serializers.ValidationError(
                "Este pasajero ya tiene un pasaje activo en este viaje."
            )

        return data

    def create(self, validated_data):
        paquetes_data = validated_data.pop("paquetes", [])
        pasaje = Pasaje.objects.create(**validated_data)

        # bulk_create para mejor performance con múltiples paquetes
        if paquetes_data:
            PaquetePasaje.objects.bulk_create(
                [PaquetePasaje(pasaje=pasaje, **paquete) for paquete in paquetes_data]
            )

        return pasaje


class PasajeAnularSerializer(serializers.Serializer):
    motivo = serializers.CharField(min_length=5, max_length=500)
