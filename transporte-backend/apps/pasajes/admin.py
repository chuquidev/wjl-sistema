from django.contrib import admin
from .models import Pasajero, Pasaje


@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = ("dni", "apellidos", "nombres", "telefono", "activo")
    search_fields = ("dni", "nombres", "apellidos")
    ordering = ("apellidos",)


@admin.register(Pasaje)
class PasajeAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "viaje",
        "pasajero",
        "asiento",
        "precio",
        "estado",
        "sucursal",
        "creado_en",
    )
    list_filter = ("estado", "sucursal", "creado_en")
    search_fields = ("pasajero__dni", "pasajero__apellidos", "codigo")
    ordering = ("-creado_en",)
    readonly_fields = ("codigo", "creado_en", "actualizado_en")
