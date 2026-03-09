from rest_framework import serializers
from django.utils import timezone
from .models import Vehiculo, Conductor, Viaje


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Vehiculo
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')


class ConductorSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField()

    class Meta:
        model  = Conductor
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')


class ViajeListSerializer(serializers.ModelSerializer):
    ruta_descripcion     = serializers.SerializerMethodField()
    vehiculo_placa       = serializers.CharField(source='vehiculo.placa', read_only=True)
    conductor_nombre     = serializers.CharField(source='conductor.nombre_completo', read_only=True)
    asientos_disponibles = serializers.SerializerMethodField()
    asientos_ocupados    = serializers.SerializerMethodField()
    precio_base          = serializers.DecimalField(
                               source='ruta.precio_base',
                               max_digits=8, decimal_places=2,
                               read_only=True
                           )
    capacidad            = serializers.IntegerField(source='vehiculo.capacidad', read_only=True)
    acepta_venta         = serializers.SerializerMethodField()  # ← nuevo

    class Meta:
        model  = Viaje
        fields = (
            'id', 'ruta', 'ruta_descripcion',
            'vehiculo', 'vehiculo_placa', 'capacidad',
            'conductor', 'conductor_nombre',
            'fecha_salida', 'fecha_llegada',
            'estado', 'precio_base',
            'asientos_disponibles', 'asientos_ocupados',
            'acepta_venta',
            'creado_en', 'activo',
        )
        read_only_fields = ('creado_en', 'actualizado_en')

    def get_ruta_descripcion(self, obj):
        try:
            return f"{obj.ruta.origen.nombre} → {obj.ruta.destino.nombre}"
        except AttributeError:
            return str(obj.ruta)

    def get_asientos_ocupados(self, obj):
        try:
            from apps.pasajes.models import Pasaje
            return Pasaje.objects.filter(
                viaje=obj,
                estado__in=['emitido', 'embarcado']
            ).count()
        except Exception:
            return 0

    def get_asientos_disponibles(self, obj):
        try:
            return obj.vehiculo.capacidad - self.get_asientos_ocupados(obj)
        except Exception:
            return 0

    def get_acepta_venta(self, obj):
        """True si todavía se pueden vender pasajes (hasta 15 min después de salida)."""
        ahora  = timezone.now()
        limite = obj.fecha_salida + timezone.timedelta(minutes=15)
        return (
            ahora <= limite and
            obj.estado not in [Viaje.Estado.COMPLETADO, Viaje.Estado.CANCELADO]
        )


class ViajeDetalleSerializer(serializers.ModelSerializer):
    ruta_descripcion     = serializers.SerializerMethodField()
    vehiculo_detalle     = VehiculoSerializer(source='vehiculo', read_only=True)
    conductor_detalle    = ConductorSerializer(source='conductor', read_only=True)
    asientos_disponibles = serializers.SerializerMethodField()
    asientos_ocupados    = serializers.SerializerMethodField()
    precio_base          = serializers.DecimalField(
                               source='ruta.precio_base',
                               max_digits=8, decimal_places=2,
                               read_only=True
                           )
    capacidad            = serializers.IntegerField(source='vehiculo.capacidad', read_only=True)

    class Meta:
        model  = Viaje
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')

    def get_ruta_descripcion(self, obj):
        try:
            return f"{obj.ruta.origen.nombre} → {obj.ruta.destino.nombre}"
        except AttributeError:
            return str(obj.ruta)

    def get_asientos_ocupados(self, obj):
        try:
            from apps.pasajes.models import Pasaje
            return Pasaje.objects.filter(
                viaje=obj,
                estado__in=['emitido', 'embarcado']
            ).count()
        except Exception:
            return 0

    def get_asientos_disponibles(self, obj):
        try:
            return obj.vehiculo.capacidad - self.get_asientos_ocupados(obj)
        except Exception:
            return 0

    def validate(self, data):
        fecha_salida  = data.get('fecha_salida')
        fecha_llegada = data.get('fecha_llegada')

        # Llegada posterior a salida
        if fecha_llegada and fecha_salida and fecha_llegada <= fecha_salida:
            raise serializers.ValidationError(
                'La fecha de llegada debe ser posterior a la fecha de salida.'
            )

        # No programar viajes en el pasado (solo en creación)
        if not self.instance and fecha_salida and fecha_salida < timezone.now():
            raise serializers.ValidationError(
                'No se puede programar un viaje con fecha de salida en el pasado.'
            )

        return data