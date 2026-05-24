from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PasajeroViewSet, PasajeViewSet

router = DefaultRouter()
router.register(r"pasajeros", PasajeroViewSet, basename="pasajero")
router.register(r"", PasajeViewSet, basename="pasaje")

urlpatterns = [
    path("", include(router.urls)),
]
