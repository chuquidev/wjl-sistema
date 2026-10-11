from rest_framework import serializers


def validar_dni(value):
    """DNI peruano: exactamente 8 dígitos."""
    if not value.isdigit() or len(value) != 8:
        raise serializers.ValidationError("El DNI debe tener exactamente 8 dígitos.")
    return value
