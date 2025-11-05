from django.shortcuts import render

from rest_framework import viewsets 
#Lo que hace es crear ViewSets de DRF, que son clases especiales que te generan automáticamente las operaciones CRUD (Crear, Leer, Actualizar, Borrar) sobre tus modelos.
from .models import Producto,Inventario
from .serializers import ProductoSerializer,InventarioSerializer
#Importa los serializers que creaste para convertir datos ↔ JSON.

#def hello(request):
   # return HttpResponse("<h1>Hello World</h1>")
#def about(request):
 #   return HttpResponse("Esta es la página About")
# en django rest framework asi se gestionan las vistas
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer