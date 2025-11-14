from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoViewSet, InventarioViewSet,
    inventario_dashboard, producto_lista, producto_crear, inventario_movimiento
)

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='api_producto')
router.register(r'movimientos', InventarioViewSet, basename='api_inventario')

urlpatterns = [
    # ===== VISTAS TEMPLATES (HTML) =====
    path('', inventario_dashboard, name='inventario_dashboard'),
    path('productos/', producto_lista, name='producto_lista'),
    path('productos/crear/', producto_crear, name='producto_crear'),
    path('movimientos/', inventario_movimiento, name='inventario_movimiento'),
    
    # ===== API REST =====
    path('api/', include(router.urls)),
]