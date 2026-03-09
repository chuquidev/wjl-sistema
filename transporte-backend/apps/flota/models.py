from django.db import models
from apps.nucleo.models import ModeloBase
from apps.ubicaciones.models import Ruta


class Vehiculo(ModeloBase):

    class Estado(models.TextChoices):
        DISPONIBLE  = 'disponible',  'Disponible'
        EN_VIAJE    = 'en_viaje',    'En viaje'
        MANTENIMIENTO = 'mantenimiento', 'En mantenimiento'
        INACTIVO    = 'inactivo',    'Inactivo'

    placa       = models.CharField(max_length=10, unique=True, verbose_name='Placa')
    marca       = models.CharField(max_length=50, verbose_name='Marca')
    modelo      = models.CharField(max_length=50, verbose_name='Modelo')
    anio        = models.PositiveSmallIntegerField(verbose_name='Año')
    capacidad   = models.PositiveSmallIntegerField(verbose_name='Capacidad de asientos')
    estado      = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.DISPONIBLE,
        verbose_name='Estado'
    )
    observacion = models.TextField(blank=True, verbose_name='Observación')

    class Meta:
        verbose_name        = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        ordering            = ['placa']

    def __str__(self):
        return f'{self.placa} - {self.marca} {self.modelo} ({self.anio})'


class Conductor(ModeloBase):

    class Estado(models.TextChoices):
        DISPONIBLE = 'disponible', 'Disponible'
        EN_VIAJE   = 'en_viaje',   'En viaje'
        INACTIVO   = 'inactivo',   'Inactivo'

    dni             = models.CharField(max_length=8, unique=True, verbose_name='DNI')
    nombres         = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos       = models.CharField(max_length=100, verbose_name='Apellidos')
    telefono        = models.CharField(max_length=15, verbose_name='Teléfono')
    licencia        = models.CharField(max_length=20, unique=True, verbose_name='N° Licencia')
    categoria_licencia = models.CharField(max_length=5, verbose_name='Categoría licencia')
    vencimiento_licencia = models.DateField(verbose_name='Vencimiento de licencia')
    estado          = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.DISPONIBLE,
        verbose_name='Estado'
    )

    class Meta:
        verbose_name        = 'Conductor'
        verbose_name_plural = 'Conductores'
        ordering            = ['apellidos', 'nombres']

    def __str__(self):
        return f'{self.apellidos}, {self.nombres} - Lic: {self.licencia}'

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'


class Viaje(ModeloBase):

    class Estado(models.TextChoices):
        PROGRAMADO  = 'programado',  'Programado'
        EN_CURSO    = 'en_curso',    'En curso'
        COMPLETADO  = 'completado',  'Completado'
        CANCELADO   = 'cancelado',   'Cancelado'

    ruta        = models.ForeignKey(
        Ruta,
        on_delete=models.PROTECT,
        related_name='viajes',
        verbose_name='Ruta'
    )
    vehiculo    = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT,
        related_name='viajes',
        verbose_name='Vehículo'
    )
    conductor   = models.ForeignKey(
        Conductor,
        on_delete=models.PROTECT,
        related_name='viajes',
        verbose_name='Conductor'
    )
    fecha_salida    = models.DateTimeField(verbose_name='Fecha y hora de salida')
    fecha_llegada   = models.DateTimeField(null=True, blank=True, verbose_name='Fecha y hora de llegada')
    estado          = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PROGRAMADO,
        verbose_name='Estado'
    )
    observacion     = models.TextField(blank=True, verbose_name='Observación')

    class Meta:
        verbose_name        = 'Viaje'
        verbose_name_plural = 'Viajes'
        ordering            = ['-fecha_salida']

    def __str__(self):
        return f'{self.ruta} | {self.fecha_salida.strftime("%d/%m/%Y %H:%M")} | {self.vehiculo.placa}'

    @property
    def asientos_disponibles(self):
        ocupados = self.pasajes.filter(
            estado__in=['emitido', 'embarcado']
        ).count()
        return self.vehiculo.capacidad - ocupados

    @property
    def asientos_ocupados(self):
        return self.pasajes.filter(
            estado__in=['emitido', 'embarcado']
        ).count()