from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
   
    # Vistas de ventas
    venta_lista, venta_crear, venta_detalle, venta_factura_pdf  # <-- AGREGADO venta_factura_pdf
)



urlpatterns = [
# Ventas
    path('', venta_lista, name='venta_lista'),
    path('crear/', venta_crear, name='venta_crear'),
    path('<int:venta_id>/', venta_detalle, name='venta_detalle'),
    # Nueva URL para factura PDF
    path('<int:venta_id>/factura/', venta_factura_pdf, name='venta_factura_pdf'),  # <-- AGREGADO
]