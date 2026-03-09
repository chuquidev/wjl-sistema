from rest_framework import serializers
from django.utils import timezone
from .models import SesionCaja, Transaccion


class TransaccionSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model            = Transaccion
        fields           = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError('El monto debe ser mayor a 0.')
        return value

    def validate(self, data):
        sesion = data.get('sesion')
        if sesion and sesion.estado == SesionCaja.Estado.CERRADA:
            raise serializers.ValidationError(
                'No se pueden registrar movimientos en una sesión de caja cerrada.'
            )
        return data


class SesionCajaListSerializer(serializers.ModelSerializer):
    cajero_nombre     = serializers.CharField(source='cajero.nombre_completo', read_only=True)
    sucursal_nombre   = serializers.CharField(source='sucursal.nombre',        read_only=True)
    total_ingresos    = serializers.ReadOnlyField()
    total_egresos     = serializers.ReadOnlyField()
    total_anulaciones = serializers.ReadOnlyField()
    saldo_esperado    = serializers.ReadOnlyField()

    class Meta:
        model  = SesionCaja
        fields = (
            'id', 'cajero', 'cajero_nombre', 'sucursal', 'sucursal_nombre',
            'monto_inicial', 'monto_final', 'estado',
            'fecha_apertura', 'fecha_cierre',
            'total_ingresos', 'total_egresos',
            'total_anulaciones', 'saldo_esperado',
            'observacion', 'activo',
        )

class SesionCajaAbrirSerializer(serializers.ModelSerializer):

    class Meta:
        model  = SesionCaja
        fields = ('monto_inicial',)

    def get_fields(self):
        from apps.ubicaciones.models import Sucursal
        fields = super().get_fields()
        fields['sucursal'] = serializers.PrimaryKeyRelatedField(
            queryset   = Sucursal.objects.filter(activo=True),
            required   = False,
            allow_null = True,
            write_only = True,
        )
        return fields

    def validate_monto_inicial(self, value):
        if value < 0:
            raise serializers.ValidationError(
                'El monto inicial no puede ser negativo.'
            )
        return value

    def validate(self, data):
        cajero   = self.context['request'].user
        es_admin = cajero.is_staff or getattr(cajero, 'rol', '') == 'administrador'

        if not es_admin and not getattr(cajero, 'sucursal', None):
            raise serializers.ValidationError(
                'Tu usuario no tiene una sucursal asignada. '
                'Contacta al administrador.'
            )

        if es_admin and not getattr(cajero, 'sucursal', None):
            if not data.get('sucursal'):
                raise serializers.ValidationError(
                    'Como administrador debes seleccionar una sucursal para abrir caja.'
                )

        if SesionCaja.objects.filter(
            cajero=cajero,
            estado=SesionCaja.Estado.ABIERTA
        ).exists():
            raise serializers.ValidationError(
                'Ya tienes una sesión de caja abierta.'
                'Ciérrala antes de abrir una nueva.'
            )

        sucursal_a_usar = (
            data.get('sucursal')
            or getattr(cajero, 'sucursal', None)
        )
        if sucursal_a_usar and SesionCaja.objects.filter(
            sucursal=sucursal_a_usar,
            estado=SesionCaja.Estado.ABIERTA
        ).exists():
            raise serializers.ValidationError(
                f'Ya hay una caja abierta en la sucursal '
                f'"{sucursal_a_usar.nombre}". '
                f'Solo puede haber una caja activa a la vez.'
            )

        return data

    def create(self, validated_data):
        cajero   = self.context['request'].user
        es_admin = cajero.is_staff or getattr(cajero, 'rol', '') == 'administrador'

        if es_admin:
            sucursal = validated_data.pop('sucursal', None) or cajero.sucursal
        else:
            validated_data.pop('sucursal', None)
            sucursal = cajero.sucursal

        validated_data['cajero']   = cajero
        validated_data['sucursal'] = sucursal
        return super().create(validated_data)
    
    
class SesionCajaCerrarSerializer(serializers.Serializer):
    monto_final = serializers.DecimalField(
        max_digits     = 10,
        decimal_places = 2,
        min_value      = 0,
        error_messages = {
            'min_value': 'El monto contado no puede ser negativo.',
        }
    )
    observacion = serializers.CharField(
        max_length  = 500,
        required    = False,
        allow_blank = True,
    )


class GastoSerializer(serializers.Serializer):
    descripcion = serializers.CharField(
        max_length = 255,
        min_length = 3,
        error_messages = {
            'min_length': 'La descripción debe tener al menos 3 caracteres.',
            'blank':      'La descripción no puede estar vacía.',
        }
    )
    monto = serializers.DecimalField(
        max_digits     = 10,
        decimal_places = 2,
        min_value      = 0.01,
        error_messages = {
            'min_value': 'El monto del gasto debe ser mayor a S/. 0.00.',
        }
    )