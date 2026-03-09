from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SesionCajaViewSet, TransaccionViewSet

router = DefaultRouter()
router.register(r'sesiones',      SesionCajaViewSet,  basename='sesion-caja')
router.register(r'transacciones', TransaccionViewSet, basename='transaccion')

urlpatterns = [
    path('', include(router.urls)),
]