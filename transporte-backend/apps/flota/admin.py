from django.contrib import admin
from .models import Vehiculo, Conductor, Viaje


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display  = ('placa', 'marca', 'modelo', 'anio', 'capacidad', 'estado', 'activo')
    list_filter   = ('estado', 'activo', 'marca')
    search_fields = ('placa', 'marca', 'modelo')
    ordering      = ('placa',)


@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display  = ('dni', 'apellidos', 'nombres', 'licencia', 'categoria_licencia', 'vencimiento_licencia', 'estado')
    list_filter   = ('estado', 'activo', 'categoria_licencia')
    search_fields = ('dni', 'nombres', 'apellidos', 'licencia')
    ordering      = ('apellidos',)


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display  = ('ruta', 'vehiculo', 'conductor', 'fecha_salida', 'estado', 'asientos_disponibles')
    list_filter   = ('estado', 'fecha_salida', 'ruta')
    search_fields = ('vehiculo__placa', 'conductor__apellidos', 'ruta__origen__nombre')
    ordering      = ('-fecha_salida',)
    readonly_fields = ('asientos_disponibles', 'asientos_ocupados')