from django.urls import path
from .views import (
    DashboardView,
    ReporteVentasView,
    ReporteCajaView,
    ExportarExcelView,
    ExportarPDFView,
)

urlpatterns = [
    path('dashboard/',       DashboardView.as_view(),      name='dashboard'),
    path('ventas/',          ReporteVentasView.as_view(),   name='reporte-ventas'),
    path('caja/',            ReporteCajaView.as_view(),     name='reporte-caja'),
    path('exportar/excel/',  ExportarExcelView.as_view(),   name='exportar-excel'),
    path('exportar/pdf/',    ExportarPDFView.as_view(),     name='exportar-pdf'),
]