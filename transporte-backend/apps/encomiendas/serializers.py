from rest_framework import serializers
from .models import Encomienda
from decimal import Decimal


class EncomiendaActualizarSerializer(serializers.Serializer):
    """
    Edición (PATCH) de una encomienda. Solo se aceptan los campos de abajo:
    estado, activo, registrado_por, sucursal_origen, etc. se ignoran, porque
    solo cambian a través de las acciones del sistema (entregar, devolver, eliminar).
    """

    remitente_nombres = serializers.CharField(max_length=100, required=False)
    remitente_apellidos = serializers.CharField(max_length=100, required=False)
    remitente_dni = serializers.CharField(max_length=8, min_length=8, required=False)
    remitente_telefono = serializers.CharField(
        max_length=15, required=False, allow_blank=True
    )
    destinatario_nombres = serializers.CharField(max_length=100, required=False)
    destinatario_apellidos = serializers.CharField(max_length=100, required=False)
    destinatario_dni = serializers.CharField(max_length=8, min_length=8, required=False)
    destinatario_telefono = serializers.CharField(
        max_length=15, required=False, allow_blank=True
    )
    descripcion = serializers.CharField(max_length=500, required=False)
    peso_kg = serializers.DecimalField(
        max_digits=6, decimal_places=2, required=False, allow_null=True
    )
    precio = serializers.DecimalField(
        max_digits=8, decimal_places=2, min_value=Decimal("0.01"), required=False
    )
    metodo_pago = serializers.ChoiceField(
        choices=["cash", "yape", "plin", "card"], required=False
    )
    viaje = serializers.IntegerField(required=False, allow_null=True)
    observacion = serializers.CharField(
        max_length=500, required=False, allow_blank=True
    )

    def _validar_dni(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El DNI debe contener solo dígitos.")
        return value

    def validate_remitente_dni(self, value):
        return self._validar_dni(value)

    def validate_destinatario_dni(self, value):
        return self._validar_dni(value)

    def validate_viaje(self, value):
        if value is None:
            return None
        # Si no cambia el viaje, no se vuelve a exigir que siga "programado"
        if value == self.instance.viaje_id:
            return self.instance.viaje
        from apps.flota.models import Viaje

        try:
            viaje = Viaje.objects.get(pk=value)
        except Viaje.DoesNotExist:
            raise serializers.ValidationError("El viaje seleccionado no existe.")
        if viaje.estado != "programado":
            raise serializers.ValidationError(
                "Solo se pueden registrar encomiendas en viajes programados."
            )
        return viaje

    def validate(self, data):
        for parte in ("remitente", "destinatario"):
            nombres = f"{parte}_nombres"
            apellidos = f"{parte}_apellidos"
            if (nombres in data) != (apellidos in data):
                raise serializers.ValidationError(
                    {nombres: f"Envía nombres y apellidos del {parte} juntos."}
                )
        dni_r = data.get("remitente_dni", self.instance.remitente_dni)
        dni_d = data.get("destinatario_dni", self.instance.destinatario_dni)
        if dni_r == dni_d:
            raise serializers.ValidationError(
                "El remitente y el destinatario no pueden tener el mismo DNI."
            )
        return data

    def update(self, instance, validated_data):
        for parte in ("remitente", "destinatario"):
            nombres = validated_data.pop(f"{parte}_nombres", None)
            apellidos = validated_data.pop(f"{parte}_apellidos", None)
            if nombres is not None:
                setattr(instance, f"{parte}_nombre", f"{nombres} {apellidos}".strip())
        for campo, valor in validated_data.items():
            setattr(instance, campo, valor)
        instance.save()
        return instance


class EncomiendaListSerializer(serializers.ModelSerializer):
    viaje_descripcion = serializers.SerializerMethodField()
    sucursal_nombre = serializers.CharField(
        source="sucursal_origen.nombre", read_only=True
    )
    registrado_por_nombre = serializers.CharField(
        source="registrado_por.nombre_completo", read_only=True
    )
    codigo_corto = serializers.SerializerMethodField()

    class Meta:
        model = Encomienda
        fields = (
            "id",
            "codigo",
            "codigo_corto",
            "viaje",
            "viaje_descripcion",
            "remitente_nombre",
            "remitente_dni",
            "remitente_telefono",
            "destinatario_nombre",
            "destinatario_dni",
            "destinatario_telefono",
            "descripcion",
            "peso_kg",
            "precio",
            "metodo_pago",
            "estado",
            "sucursal_origen",
            "sucursal_nombre",
            "registrado_por",
            "registrado_por_nombre",
            "fecha_entrega",
            "entregado_a",
            "observacion",
            "creado_en",
            "activo",
        )

    def get_codigo_corto(self, obj):
        return str(obj.codigo)[:8].upper()

    def get_viaje_descripcion(self, obj):
        if not obj.viaje:
            return None
        try:
            ruta = obj.viaje.ruta
            if obj.viaje.fecha_salida:
                import pytz

                peru_tz = pytz.timezone("America/Lima")
                fecha_local = obj.viaje.fecha_salida.astimezone(peru_tz)
                fecha = fecha_local.strftime("%d/%m/%Y %I:%M %p")
            else:
                fecha = ""
            placa = obj.viaje.vehiculo.placa if obj.viaje.vehiculo else ""
            return f"{ruta.origen.nombre} -> {ruta.destino.nombre} | {fecha} | {placa}"
        except Exception:
            return str(obj.viaje)


class EncomiendaCrearSerializer(serializers.Serializer):
    # Remitente
    remitente_nombres = serializers.CharField(max_length=100)
    remitente_apellidos = serializers.CharField(max_length=100)
    remitente_dni = serializers.CharField(max_length=8, min_length=8)
    remitente_telefono = serializers.CharField(
        max_length=15, required=False, allow_blank=True, default=""
    )

    # Destinatario
    destinatario_nombres = serializers.CharField(max_length=100)
    destinatario_apellidos = serializers.CharField(max_length=100)
    destinatario_dni = serializers.CharField(max_length=8, min_length=8)
    destinatario_telefono = serializers.CharField(
        max_length=15, required=False, allow_blank=True, default=""
    )

    # Encomienda
    descripcion = serializers.CharField(max_length=500)
    peso_kg = serializers.DecimalField(
        max_digits=6, decimal_places=2, required=False, allow_null=True
    )
    precio = serializers.DecimalField(max_digits=8, decimal_places=2, min_value=0.01)
    metodo_pago = serializers.ChoiceField(choices=["cash", "yape", "plin", "card"])
    viaje = serializers.IntegerField(required=False, allow_null=True)
    observacion = serializers.CharField(
        max_length=500, required=False, allow_blank=True, default=""
    )

    def validate_remitente_dni(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El DNI debe contener solo dígitos.")
        return value

    def validate_destinatario_dni(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El DNI debe contener solo dígitos.")
        return value

    def validate_viaje(self, value):
        if value is None:
            return None
        from apps.flota.models import Viaje

        try:
            viaje = Viaje.objects.get(pk=value)
        except Viaje.DoesNotExist:
            raise serializers.ValidationError("El viaje seleccionado no existe.")
        if viaje.estado != "programado":
            raise serializers.ValidationError(
                "Solo se pueden registrar encomiendas en viajes programados."
            )
        return viaje

    def validate(self, data):
        if data.get("remitente_dni") == data.get("destinatario_dni"):
            raise serializers.ValidationError(
                "El remitente y el destinatario no pueden tener el mismo DNI."
            )
        return data

    def create(self, validated_data):
        usuario = self.context["request"].user
        if not getattr(usuario, "sucursal", None):
            raise serializers.ValidationError(
                "Tu usuario no tiene una sucursal asignada. Contacta al administrador."
            )
        remitente_nombre = f"{validated_data['remitente_nombres']} {validated_data['remitente_apellidos']}".strip()
        destinatario_nombre = f"{validated_data['destinatario_nombres']} {validated_data['destinatario_apellidos']}".strip()

        return Encomienda.objects.create(
            remitente_nombre=remitente_nombre,
            remitente_dni=validated_data["remitente_dni"],
            remitente_telefono=validated_data.get("remitente_telefono", ""),
            destinatario_nombre=destinatario_nombre,
            destinatario_dni=validated_data["destinatario_dni"],
            destinatario_telefono=validated_data.get("destinatario_telefono", ""),
            descripcion=validated_data["descripcion"],
            peso_kg=validated_data.get("peso_kg"),
            precio=validated_data["precio"],
            metodo_pago=validated_data["metodo_pago"],
            viaje=validated_data.get("viaje"),
            observacion=validated_data.get("observacion", ""),
            registrado_por=usuario,
            sucursal_origen=usuario.sucursal,
        )


class EncomiendaEntregarSerializer(serializers.Serializer):
    entregado_a = serializers.CharField(max_length=150)
