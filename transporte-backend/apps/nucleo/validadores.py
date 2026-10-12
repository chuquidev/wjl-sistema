from rest_framework import serializers


def validar_dni(value):
    """DNI peruano: exactamente 8 dígitos."""
    if not value.isdigit() or len(value) != 8:
        raise serializers.ValidationError("El DNI debe tener exactamente 8 dígitos.")
    return value


def validar_telefono(value):
    """Teléfono opcional: 6 a 15 dígitos, con + inicial y espacios permitidos."""
    limpio = value.replace(" ", "")
    if limpio and not (
        limpio.lstrip("+").isdigit() and 9 <= len(limpio.lstrip("+")) <= 9
    ):
        raise serializers.ValidationError(
            "El teléfono debe tener entre 6 y 15 dígitos (solo números)."
        )
    return value.strip()
