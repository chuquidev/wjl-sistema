from rest_framework import serializers


def validar_dni(value):
    """DNI peruano: exactamente 8 dígitos."""
    if not value.isdigit() or len(value) != 8:
        raise serializers.ValidationError("El DNI debe tener exactamente 8 dígitos.")
    return value


def validar_telefono(value):
    """Teléfono opcional: celular peruano de 9 dígitos."""
    limpio = value.replace(" ", "")
    if limpio and not (limpio.isdigit() and len(limpio) == 9):
        raise serializers.ValidationError("El teléfono debe tener 9 dígitos.")
    return value.strip()
