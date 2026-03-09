from django.db import models
from apps.nucleo.models import ModeloBase


class Sucursal(ModeloBase):
    nombre       = models.CharField(max_length=100, verbose_name='Nombre')
    direccion    = models.CharField(max_length=200, verbose_name='Dirección')
    ciudad       = models.CharField(max_length=100, verbose_name='Ciudad')
    telefono     = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    es_principal = models.BooleanField(default=False, verbose_name='Es principal')

    class Meta:
        verbose_name        = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering            = ['nombre']

    def __str__(self):
        return self.nombre


class Ciudad(ModeloBase):
    nombre       = models.CharField(max_length=100, verbose_name='Nombre')
    departamento = models.CharField(max_length=100, verbose_name='Departamento')

    class Meta:
        verbose_name        = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering            = ['nombre']

    def __str__(self):
        return f'{self.nombre} - {self.departamento}'


class Ruta(ModeloBase):
    origen         = models.ForeignKey(Ciudad, on_delete=models.PROTECT, related_name='rutas_origen',  verbose_name='Origen')
    destino        = models.ForeignKey(Ciudad, on_delete=models.PROTECT, related_name='rutas_destino', verbose_name='Destino')
    precio_base    = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Precio base (S/.)')
    duracion_horas = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Duración (horas)')
    distancia_km   = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='Distancia (km)')

    class Meta:
        verbose_name        = 'Ruta'
        verbose_name_plural = 'Rutas'
        unique_together     = ('origen', 'destino')
        ordering            = ['origen__nombre']

    def __str__(self):
        return f'{self.origen} → {self.destino}'


class Parada(ModeloBase):
    ruta   = models.ForeignKey(Ruta,   on_delete=models.CASCADE,  related_name='paradas', verbose_name='Ruta')
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT,                           verbose_name='Ciudad')
    orden  = models.PositiveSmallIntegerField(verbose_name='Orden')
    precio = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Precio desde origen (S/.)')

    class Meta:
        verbose_name        = 'Parada'
        verbose_name_plural = 'Paradas'
        ordering            = ['ruta', 'orden']
        unique_together     = ('ruta', 'orden')

    def __str__(self):
        return f'{self.ruta} | Parada {self.orden}: {self.ciudad}'