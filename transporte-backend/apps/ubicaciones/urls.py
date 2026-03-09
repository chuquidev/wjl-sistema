from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SucursalViewSet, CiudadViewSet, RutaViewSet, ParadaViewSet

router = DefaultRouter()
router.register(r'sucursales', SucursalViewSet, basename='sucursal')
router.register(r'ciudades',   CiudadViewSet,   basename='ciudad')
router.register(r'rutas',      RutaViewSet,     basename='ruta')
router.register(r'paradas',    ParadaViewSet,   basename='parada')

urlpatterns = [
    path('', include(router.urls)),
]