from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from apps.usuarios.views import TokenPorCorreoView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Reemplaza TokenObtainPairView por TokenPorCorreoView
    path("api/v1/auth/token/", TokenPorCorreoView.as_view(), name="token_obtener"),
    # Autenticación JWT
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtener"),
    path(
        "api/v1/auth/token/refrescar/",
        TokenRefreshView.as_view(),
        name="token_refrescar",
    ),
    path(
        "api/v1/auth/token/cerrar/", TokenBlacklistView.as_view(), name="token_cerrar"
    ),
    # Apps
    path("api/v1/usuarios/", include("apps.usuarios.urls")),
    path("api/v1/ubicaciones/", include("apps.ubicaciones.urls")),
    path("api/v1/flota/", include("apps.flota.urls")),
    path("api/v1/pasajes/", include("apps.pasajes.urls")),
    path("api/v1/encomiendas/", include("apps.encomiendas.urls")),
    path("api/v1/caja/", include("apps.caja.urls")),
    path("api/v1/reportes/", include("apps.reportes.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
