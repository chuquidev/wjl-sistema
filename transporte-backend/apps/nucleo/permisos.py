from rest_framework.permissions import BasePermission, SAFE_METHODS


def es_administrador(user):
    """True si el usuario autenticado es administrador (rol o is_staff)."""
    return bool(
        user
        and user.is_authenticated
        and (user.is_staff or getattr(user, "rol", "") == "administrador")
    )


def es_supervisor(user):
    return bool(
        user and user.is_authenticated and getattr(user, "rol", "") == "supervisor"
    )


class EsAdministrador(BasePermission):
    """Solo administradores (lectura y escritura)."""

    message = "Solo un administrador puede realizar esta acción."

    def has_permission(self, request, view):
        return es_administrador(request.user)


class LecturaAutenticadoEscrituraAdmin(BasePermission):
    """
    Cualquier usuario autenticado puede LEER (GET/HEAD/OPTIONS).
    Solo el administrador puede CREAR, MODIFICAR o ELIMINAR.
    """

    message = "Solo un administrador puede modificar estos datos."

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return es_administrador(user)


class LecturaAutenticadoEscrituraGestion(BasePermission):
    """
    Cualquier usuario autenticado puede LEER.
    Solo administrador o supervisor pueden CREAR, MODIFICAR o ELIMINAR.
    """

    message = "Solo un administrador o supervisor puede modificar estos datos."

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return es_administrador(user) or es_supervisor(user)


