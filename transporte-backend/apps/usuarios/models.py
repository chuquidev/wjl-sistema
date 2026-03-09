from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from apps.nucleo.models import ModeloBase


class ManagerUsuario(BaseUserManager):

    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio.')
        correo  = self.normalize_email(correo)
        usuario = self.model(correo=correo, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',     True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol',          Usuario.Rol.ADMINISTRADOR)
        return self.create_user(correo, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin, ModeloBase):

    class Rol(models.TextChoices):
        ADMINISTRADOR = 'administrador', 'Administrador'
        SUPERVISOR    = 'supervisor',    'Supervisor'
        CAJERO        = 'cajero',        'Cajero'

    correo    = models.EmailField(unique=True,    verbose_name='Correo electrónico')
    nombres   = models.CharField(max_length=100,  verbose_name='Nombres')
    apellidos = models.CharField(max_length=100,  verbose_name='Apellidos')
    dni       = models.CharField(max_length=8, unique=True, verbose_name='DNI')
    telefono  = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    rol       = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.CAJERO,
        verbose_name='Rol'
    )
    sucursal  = models.ForeignKey(
        'ubicaciones.Sucursal',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='usuarios',
        verbose_name='Sucursal'
    )
    is_staff = models.BooleanField(default=False, verbose_name='Es staff')

    objects = ManagerUsuario()

    USERNAME_FIELD  = 'correo'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'dni']

    class Meta:
        verbose_name        = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering            = ['apellidos', 'nombres']

    def __str__(self):
        return f'{self.apellidos}, {self.nombres} ({self.get_rol_display()})'

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'