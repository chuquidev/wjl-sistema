from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flota", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conductor",
            name="categoria_licencia",
            field=models.CharField(max_length=10, verbose_name="Categoría licencia"),
        ),
    ]
