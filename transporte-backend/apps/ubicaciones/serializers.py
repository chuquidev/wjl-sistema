from rest_framework import serializers
from .models import Sucursal, Ciudad, Ruta, Parada


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Sucursal
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')


class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Ciudad
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')


class ParadaSerializer(serializers.ModelSerializer):
    ciudad_nombre = serializers.CharField(source='ciudad.nombre', read_only=True)

    class Meta:
        model  = Parada
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')


class RutaSerializer(serializers.ModelSerializer):
    origen_nombre  = serializers.CharField(source='origen.nombre',  read_only=True)
    destino_nombre = serializers.CharField(source='destino.nombre', read_only=True)
    paradas        = ParadaSerializer(many=True, read_only=True)

    class Meta:
        model  = Ruta
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')