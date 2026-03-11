import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from decouple import config

User = get_user_model()

class Command(BaseCommand):
    help = "Crea el superadmin inicial para el sistema de transporte (WJL)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            help="Email del superadmin (sobrescribe el .env)",
        )
        parser.add_argument(
            "--password",
            type=str,
            help="Password del superadmin (sobrescribe el .env)",
        )
        parser.add_argument(
            "--dni",
            type=str,
            default="99999999",
            help="DNI requerido por el modelo Usuario (default: 99999999)",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Elimina y recrea el superadmin si ya existe por correo",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        # Obtener credenciales (Prioridad: Argumentos > .env)
        # decouple busca automáticamente en el archivo .env
        email = options["email"] or config("SUPERADMIN_EMAIL", default=None)
        password = options["password"] or config("SUPERADMIN_PASSWORD", default=None)
        dni = options["dni"]

        # Validar variables críticas
        if not email or not password:
            self.stderr.write(self.style.ERROR(
                "❌ Error: El EMAIL y PASSWORD son obligatorios. "
                "Defínelos en el .env o pásalos como --email y --password."
            ))
            return

        # 2. Verificar existencia usando 'correo' (tu campo real)
        # Tu modelo no tiene campo 'username', por eso fallaba el anterior.
        usuario_existente = User.objects.filter(correo=email).first()

        if usuario_existente:
            if options["force"]:
                usuario_existente.delete()
                self.stdout.write(self.style.WARNING(
                    f'⚠️ Usuario con correo "{email}" eliminado para recrear.'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'⚠️ El superadmin con correo "{email}" ya existe. '
                    "Usa --force para recrearlo."
                ))
                return

        # 3. Crear el Superusuario con los campos de tu modelo
        try:
            # create_superuser llama internamente a tu ManagerUsuario.create_superuser
            User.objects.create_superuser(
                correo=email,
                password=password,
                nombres="Administrador",
                apellidos="Sistema",
                dni=dni,
                rol=User.Rol.ADMINISTRADOR  # Usamos el Enum de tu modelo
            )

            self.stdout.write(self.style.SUCCESS(
                f'✅ Superadmin "{email}" creado exitosamente con DNI {dni}.'
            ))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error al crear superusuario: {str(e)}"))