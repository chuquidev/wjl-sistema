from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Usuario
from apps.nucleo.validadores import validar_dni, validar_telefono


def _exigir_sucursal_a_cajero(rol, sucursal):
    """Un cajero sin sucursal no puede abrir caja ni vender."""
    if rol == Usuario.Rol.CAJERO and not sucursal:
        raise serializers.ValidationError(
            {"sucursal": "Un cajero debe tener una sucursal asignada."}
        )


class UsuarioListSerializer(serializers.ModelSerializer):
    sucursal_nombre = serializers.CharField(source="sucursal.nombre", read_only=True)
    rol_display = serializers.CharField(source="get_rol_display", read_only=True)
    nombre_completo = serializers.ReadOnlyField()

    class Meta:
        model = Usuario
        fields = (
            "id",
            "correo",
            "nombres",
            "apellidos",
            "nombre_completo",
            "dni",
            "telefono",
            "rol",
            "rol_display",
            "sucursal",
            "sucursal_nombre",
            "is_staff",
            "activo",
            "creado_en",
        )


class UsuarioCrearSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirmar_password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = (
            "correo",
            "nombres",
            "apellidos",
            "dni",
            "telefono",
            "rol",
            "sucursal",
            "password",
            "confirmar_password",
        )

    def validate_dni(self, value):
        return validar_dni(value)

    def validate_telefono(self, value):
        return validar_telefono(value)

    def validate(self, data):
        _exigir_sucursal_a_cajero(data.get("rol"), data.get("sucursal"))
        if data["password"] != data.pop("confirmar_password"):
            raise serializers.ValidationError(
                {"confirmar_password": "Las contraseñas no coinciden."}
            )
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario


class UsuarioActualizarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            "nombres",
            "apellidos",
            "telefono",
            "rol",
            "sucursal",
            "activo",
        )

    def validate_telefono(self, value):
        return validar_telefono(value)

    def validate(self, data):
        usuario = self.instance
        rol = data.get("rol", usuario.rol)
        sucursal = data["sucursal"] if "sucursal" in data else usuario.sucursal
        _exigir_sucursal_a_cajero(rol, sucursal)

        # Un administrador no puede bloquearse a sí mismo
        if usuario == self.context["request"].user:
            if data.get("activo") is False:
                raise serializers.ValidationError(
                    {"activo": "No puedes desactivarte a ti mismo."}
                )
            if rol != Usuario.Rol.ADMINISTRADOR and not usuario.is_staff:
                raise serializers.ValidationError(
                    {"rol": "No puedes quitarte tu propio rol de administrador."}
                )
        return data


class RestablecerPasswordSerializer(serializers.Serializer):
    """El administrador define una clave nueva para otro usuario."""

    password_nuevo = serializers.CharField(write_only=True)
    confirmar_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password_nuevo"] != data["confirmar_password"]:
            raise serializers.ValidationError(
                {"confirmar_password": "Las contraseñas no coinciden."}
            )
        # Se valida contra el usuario destino (no permite claves parecidas a su correo/nombre)
        try:
            validate_password(data["password_nuevo"], user=self.context["usuario"])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password_nuevo": list(e.messages)})
        return data


class CambiarPasswordSerializer(serializers.Serializer):
    password_actual = serializers.CharField(write_only=True)
    password_nuevo = serializers.CharField(
        write_only=True, validators=[validate_password]
    )
    confirmar_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password_nuevo"] != data["confirmar_password"]:
            raise serializers.ValidationError(
                {"confirmar_password": "Las contraseñas no coinciden."}
            )
        usuario = self.context["request"].user
        if data["password_nuevo"] == data["password_actual"]:
            raise serializers.ValidationError(
                {
                    "password_nuevo": "La nueva contraseña debe ser distinta de la actual."
                }
            )
        # Valida también contra los datos del usuario (correo, nombres, DNI...)
        try:
            validate_password(data["password_nuevo"], user=usuario)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password_nuevo": list(e.messages)})
        return data


class PerfilSerializer(serializers.ModelSerializer):
    sucursal_nombre = serializers.CharField(source="sucursal.nombre", read_only=True)
    rol_display = serializers.CharField(source="get_rol_display", read_only=True)
    nombre_completo = serializers.ReadOnlyField()

    class Meta:
        model = Usuario
        fields = (
            "id",
            "correo",
            "nombres",
            "apellidos",
            "nombre_completo",
            "dni",
            "telefono",
            "rol",
            "rol_display",
            "sucursal",
            "sucursal_nombre",
            "creado_en",
        )
        # Solo nombres, apellidos y telefono son editables
        read_only_fields = (
            "id",
            "correo",
            "dni",
            "rol",
            "rol_display",
            "sucursal",
            "sucursal_nombre",
            "nombre_completo",
            "creado_en",
        )

    def validate_telefono(self, value):
        return validar_telefono(value)


class TokenPorCorreoSerializer(TokenObtainPairSerializer):
    username_field = "correo"
