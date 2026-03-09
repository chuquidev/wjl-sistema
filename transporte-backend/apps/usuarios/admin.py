from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model         = Usuario
    list_display  = ('correo', 'apellidos', 'nombres', 'rol', 'sucursal', 'activo')
    list_filter   = ('rol', 'sucursal', 'activo')
    search_fields = ('correo', 'nombres', 'apellidos', 'dni')
    ordering      = ('apellidos',)

    fieldsets = (
        ('Acceso', {'fields': ('correo', 'password')}),
        ('Datos personales', {'fields': ('nombres', 'apellidos', 'dni', 'telefono')}),
        ('Rol y sucursal', {'fields': ('rol', 'sucursal')}),
        ('Permisos', {'fields': ('is_staff', 'is_superuser', 'activo', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('correo', 'nombres', 'apellidos', 'dni', 'rol', 'sucursal', 'password1', 'password2'),
        }),
    )