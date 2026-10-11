from django.db import migrations, models


def verificar_sin_duplicados(apps, schema_editor):
    """
    Antes de crear la restricción, comprueba que no existan asientos ya vendidos
    dos veces (la doble venta era posible antes de esta migración). Si los hay,
    aborta con un mensaje claro: hay que decidir a mano cuál pasaje es el válido
    (anulando el otro) porque hay dinero de por medio.
    """
    Pasaje = apps.get_model("pasajes", "Pasaje")
    duplicados = (
        Pasaje.objects.filter(estado__in=["emitido", "embarcado"])
        .values("viaje_id", "asiento")
        .annotate(total=models.Count("id"))
        .filter(total__gt=1)
    )
    if not duplicados.exists():
        return

    detalle = []
    for d in duplicados:
        ids = list(
            Pasaje.objects.filter(
                viaje_id=d["viaje_id"],
                asiento=d["asiento"],
                estado__in=["emitido", "embarcado"],
            ).values_list("id", flat=True)
        )
        detalle.append(f"viaje {d['viaje_id']}, asiento {d['asiento']}: pasajes {ids}")

    raise RuntimeError(
        "No se puede crear la restricción de asiento único: hay asientos vendidos "
        "dos veces. Anula (estado='anulado') el pasaje que no corresponda y vuelve "
        "a ejecutar 'python manage.py migrate'.\n  - " + "\n  - ".join(detalle)
    )


class Migration(migrations.Migration):

    dependencies = [
        ("pasajes", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(verificar_sin_duplicados, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="pasaje",
            constraint=models.UniqueConstraint(
                condition=models.Q(("estado__in", ["emitido", "embarcado"])),
                fields=("viaje", "asiento"),
                name="pasaje_asiento_unico_activo",
            ),
        ),
    ]
