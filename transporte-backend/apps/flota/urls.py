from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculoViewSet, ConductorViewSet, ViajeViewSet

router = DefaultRouter()
router.register(r'vehiculos',  VehiculoViewSet,  basename='vehiculo')
router.register(r'conductores', ConductorViewSet, basename='conductor')
router.register(r'viajes',     ViajeViewSet,     basename='viaje')

urlpatterns = [
    path('', include(router.urls)),
]