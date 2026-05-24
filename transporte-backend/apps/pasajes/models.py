import uuid
from django.db import models
from apps.nucleo.models import ModeloBase
from apps.flota.models import Viaje


class Pasajero(ModeloBase):
    dni = models.CharField(max_length=8, unique=True, verbose_name="DNI")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    telefono = models.CharField(max_length=15, blank=True, verbose_name="Teléfono")

    class Meta:
        verbose_name = "Pasajero"
        verbose_name_plural = "Pasajeros"
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return f"{self.apellidos}, {self.nombres} - DNI: {self.dni}"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"


class Pasaje(ModeloBase):

    class Estado(models.TextChoices):
        EMITIDO = "emitido", "Emitido"
        EMBARCADO = "embarcado", "Embarcado"
        ANULADO = "anulado", "Anulado"

    class MetodoPago(models.TextChoices):
        CASH = "cash", "Efectivo"
        YAPE = "yape", "Yape"
        PLIN = "plin", "Plin"
        CARD = "card", "Tarjeta"

    codigo = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="Código"
    )
    viaje = models.ForeignKey(
        Viaje, on_delete=models.PROTECT, related_name="pasajes", verbose_name="Viaje"
    )
    pasajero = models.ForeignKey(
        Pasajero,
        on_delete=models.PROTECT,
        related_name="pasajes",
        verbose_name="Pasajero",
    )
    asiento = models.PositiveSmallIntegerField(verbose_name="N° Asiento")
    precio = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Precio (S/.)"
    )
    metodo_pago = models.CharField(
        max_length=10,
        choices=MetodoPago.choices,
        default=MetodoPago.CASH,
        verbose_name="Método de pago",
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.EMITIDO,
        verbose_name="Estado",
    )
    vendido_por = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.PROTECT,
        related_name="pasajes_vendidos",
        verbose_name="Vendido por",
    )
    sucursal = models.ForeignKey(
        "ubicaciones.Sucursal",
        on_delete=models.PROTECT,
        related_name="pasajes",
        verbose_name="Sucursal",
    )
    motivo_anulacion = models.TextField(blank=True, verbose_name="Motivo de anulación")

    class Meta:
        verbose_name = "Pasaje"
        verbose_name_plural = "Pasajes"
        ordering = ["-creado_en"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio__gt=0), name="pasaje_precio_positivo"
            )
        ]

    def __str__(self):
        return f"Pasaje {str(self.codigo)[:8].upper()} - {self.pasajero} - Asiento {self.asiento}"

    @property
    def tiene_paquetes(self):
        return self.paquetes.filter(activo=True).exists()

    @property
    def total_paquetes(self):
        return (
            self.paquetes.filter(activo=True).aggregate(
                total=models.Sum("precio_adicional")
            )["total"]
            or 0
        )


class PaquetePasaje(ModeloBase):
    """Paquetes/bultos adicionales que lleva un pasajero en su pasaje."""

    pasaje = models.ForeignKey(
        Pasaje, on_delete=models.CASCADE, related_name="paquetes", verbose_name="Pasaje"
    )
    descripcion = models.CharField(
        max_length=200, verbose_name="Descripción del contenido"
    )
    cantidad_bultos = models.PositiveSmallIntegerField(
        default=1, verbose_name="Cantidad de bultos"
    )
    peso_kg = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)"
    )
    precio_adicional = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Precio adicional (S/.)"
    )

    class Meta:
        verbose_name = "Paquete de pasaje"
        verbose_name_plural = "Paquetes de pasaje"
        ordering = ["creado_en"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio_adicional__gte=0),
                name="paquete_precio_no_negativo",
            ),
            models.CheckConstraint(
                condition=models.Q(cantidad_bultos__gte=1),
                name="paquete_cantidad_minima",
            ),
        ]

    def __str__(self):
        return f"{self.cantidad_bultos} bulto(s) - {self.descripcion} - S/. {self.precio_adicional}"
