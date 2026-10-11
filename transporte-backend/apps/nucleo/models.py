from django.db import models


class ModeloBase(models.Model):
    """Modelo abstracto base con campos de auditoría para todas las entidades."""

    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        abstract = True
