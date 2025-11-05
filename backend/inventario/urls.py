from django.contrib import admin


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, InventarioViewSet

router =DefaultRouter() #esta crenado un espacio en el router para registras visttas
router.register(r'Productos',ProductoViewSet)
router.register(r'Inventario',InventarioViewSet)
urlpatterns = [
  
    path('api/', include(router.urls)),  # 👈 Aquí sí debe ir esta línea
]