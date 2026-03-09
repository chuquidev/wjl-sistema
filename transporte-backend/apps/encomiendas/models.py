import uuid
from django.db import models
from apps.nucleo.models import ModeloBase
from apps.flota.models import Viaje


class Encomienda(ModeloBase):

    class Estado(models.TextChoices):
        REGISTRADA  = 'registrada',  'Registrada'
        EN_TRANSITO = 'en_transito', 'En tránsito'
        ENTREGADA   = 'entregada',   'Entregada'
        DEVUELTA    = 'devuelta',    'Devuelta'

    codigo = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, verbose_name='Código de rastreo'
    )

    # FIX: viaje opcional
    viaje = models.ForeignKey(
        Viaje, on_delete=models.PROTECT,
        related_name='encomiendas', verbose_name='Viaje',
        null=True, blank=True,
    )

    remitente_nombre   = models.CharField(max_length=150, verbose_name='Remitente')
    remitente_dni      = models.CharField(max_length=8, verbose_name='DNI remitente')
    remitente_telefono = models.CharField(max_length=15, blank=True, verbose_name='Teléfono remitente')

    destinatario_nombre   = models.CharField(max_length=150, verbose_name='Destinatario')
    destinatario_dni      = models.CharField(max_length=8, verbose_name='DNI destinatario')
    destinatario_telefono = models.CharField(max_length=15, blank=True, verbose_name='Teléfono destinatario')

    descripcion = models.TextField(verbose_name='Descripción del contenido')

    # FIX: peso_kg opcional
    peso_kg = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=True, blank=True, verbose_name='Peso (kg)'
    )

    precio = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Precio (S/.)')

    # FIX: campo metodo_pago que faltaba
    metodo_pago = models.CharField(
        max_length=10,
        choices=[('cash','Efectivo'),('yape','Yape'),('plin','Plin'),('card','Tarjeta')],
        default='cash', verbose_name='Método de pago'
    )

    estado = models.CharField(
        max_length=20, choices=Estado.choices,
        default=Estado.REGISTRADA, verbose_name='Estado'
    )
    observacion     = models.TextField(blank=True, verbose_name='Observación')
    registrado_por  = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT, related_name='encomiendas_registradas')
    sucursal_origen = models.ForeignKey('ubicaciones.Sucursal', on_delete=models.PROTECT, related_name='encomiendas_origen')
    fecha_entrega   = models.DateTimeField(null=True, blank=True)
    entregado_a     = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name        = 'Encomienda'
        verbose_name_plural = 'Encomiendas'
        ordering            = ['-creado_en']
        constraints = [
            models.CheckConstraint(condition=models.Q(precio__gt=0), name='encomienda_precio_positivo'),
        ]

    def __str__(self):
        return f'Enc. {str(self.codigo)[:8].upper()} - {self.remitente_nombre} → {self.destinatario_nombre}'