from django.db import models
from apps.nucleo.models import ModeloBase


class SesionCaja(ModeloBase):

    class Estado(models.TextChoices):
        ABIERTA  = 'abierta',  'Abierta'
        CERRADA  = 'cerrada',  'Cerrada'

    cajero        = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.PROTECT,
        related_name='sesiones_caja',
        verbose_name='Cajero'
    )
    sucursal      = models.ForeignKey(
        'ubicaciones.Sucursal',
        on_delete=models.PROTECT,
        related_name='sesiones_caja',
        verbose_name='Sucursal'
    )
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto inicial (S/.)')
    monto_final   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Monto final real (S/.)')
    estado        = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.ABIERTA,
        verbose_name='Estado'
    )
    fecha_apertura = models.DateTimeField(auto_now_add=True, verbose_name='Fecha apertura')
    fecha_cierre   = models.DateTimeField(null=True, blank=True, verbose_name='Fecha cierre')
    observacion    = models.TextField(blank=True, verbose_name='Observación al cierre')

    class Meta:
        verbose_name        = 'Sesión de caja'
        verbose_name_plural = 'Sesiones de caja'
        ordering            = ['-fecha_apertura']

    def __str__(self):
        return f'Caja {self.sucursal} - {self.cajero} - {self.fecha_apertura.strftime("%d/%m/%Y")}'

    @property
    def total_ingresos(self):
        return self.transacciones.filter(
            tipo__in=['venta_pasaje', 'venta_encomienda']
        ).aggregate(
            total=models.Sum('monto')
        )['total'] or 0

    @property
    def total_egresos(self):
        return self.transacciones.filter(
            tipo='gasto'
        ).aggregate(
            total=models.Sum('monto')
        )['total'] or 0

    @property
    def total_anulaciones(self):
        return self.transacciones.filter(
            tipo='anulacion'
        ).aggregate(
            total=models.Sum('monto')
        )['total'] or 0

    @property
    def saldo_esperado(self):
        return self.monto_inicial + self.total_ingresos - self.total_egresos - self.total_anulaciones


class Transaccion(ModeloBase):

    class Tipo(models.TextChoices):
        VENTA_PASAJE      = 'venta_pasaje',      'Venta de pasaje'
        VENTA_ENCOMIENDA  = 'venta_encomienda',  'Venta de encomienda'
        GASTO             = 'gasto',             'Gasto'
        ANULACION         = 'anulacion',         'Anulación'

    sesion      = models.ForeignKey(
        SesionCaja,
        on_delete=models.PROTECT,
        related_name='transacciones',
        verbose_name='Sesión de caja'
    )
    tipo        = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        verbose_name='Tipo'
    )
    monto       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto (S/.)')
    descripcion = models.CharField(max_length=255, verbose_name='Descripción')
    referencia_pasaje     = models.ForeignKey(
        'pasajes.Pasaje',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='transacciones',
        verbose_name='Pasaje referencia'
    )
    referencia_encomienda = models.ForeignKey(
        'encomiendas.Encomienda',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='transacciones',
        verbose_name='Encomienda referencia'
    )

    class Meta:
        verbose_name        = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering            = ['-creado_en']
        constraints         = [
            models.CheckConstraint(
                condition=models.Q(monto__gt=0),
                name='transaccion_monto_positivo'
            )
        ]

    def __str__(self):
        return f'{self.get_tipo_display()} - S/. {self.monto} - {self.creado_en.strftime("%d/%m/%Y %H:%M")}'