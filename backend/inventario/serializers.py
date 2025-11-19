from rest_framework import serializers
from .models import Producto, Inventario

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):

    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)  # 👈 solo lectura
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())     # 👈 editable por id

    class Meta:
        model = Inventario
        fields = ['id', 'producto', 'producto_nombre', 'tipo', 'cantidad']

