from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import viewsets 
from .models import Producto, Inventario
from .serializers import ProductoSerializer, InventarioSerializer


# ==================== VISTAS API (REST) ====================

class ProductoViewSet(viewsets.ModelViewSet):
    """API CRUD para Productos"""
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
class InventarioViewSet(viewsets.ModelViewSet):
    """API CRUD para Movimientos de Inventario"""
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer


# ==================== VISTAS BASADAS EN TEMPLATES ====================

@login_required(login_url='login')
def inventario_dashboard(request):
    """Dashboard principal del inventario"""
    productos = Producto.objects.all()
    movimientos = Inventario.objects.all().order_by('-id')
    
    context = {
        'productos': productos,
        'movimientos': movimientos,
        'total_productos': productos.count(),
        'stock_total': sum([p.stock for p in productos])
    }
    return render(request, 'inventario/dashboard.html', context)


@login_required(login_url='login')
def producto_lista(request):
    """Lista de productos con stock"""
    productos = Producto.objects.all()
    return render(request, 'inventario/producto_lista.html', {'productos': productos})


@login_required(login_url='login')
def producto_crear(request):
    """Crear nuevo producto"""
    if request.method == 'POST':
        try:
            codigo = request.POST.get('codigo').strip()
            nombre = request.POST.get('nombre').strip()
            precio_compra = request.POST.get('precio_compra').strip()
            precio_venta = request.POST.get('precio_venta').strip()
            
            # Validaciones
            if not all([codigo, nombre, precio_compra, precio_venta]):
                messages.error(request, 'Por favor completa todos los campos')
                return render(request, 'inventario/producto_form.html')
            
            if Producto.objects.filter(codigo=codigo).exists():
                messages.error(request, 'El código ya existe')
                return render(request, 'inventario/producto_form.html')
            
            Producto.objects.create(
                codigo=int(codigo),
                nombre=nombre,
                precio_compra=float(precio_compra),
                precio_venta=float(precio_venta),
                stock=0
            )
            messages.success(request, f'Producto "{nombre}" creado exitosamente')
            return redirect('producto_lista')
        except ValueError:
            messages.error(request, 'Códigos y precios deben ser números')
            return render(request, 'inventario/producto_form.html')
    
    return render(request, 'inventario/producto_form.html')


@login_required(login_url='login')
def inventario_movimiento(request):
    """Crear movimiento de inventario (entrada/salida)"""
    if request.method == 'POST':
        try:
            producto_id = request.POST.get('producto_id').strip()
            tipo = request.POST.get('tipo').strip()
            cantidad = request.POST.get('cantidad').strip()
            numero_referencia = request.POST.get('numero_referencia').strip()
            
            # Validaciones
            if not all([producto_id, tipo, cantidad]):
                messages.error(request, 'Por favor completa todos los campos')
                return render(request, 'inventario/movimiento_form.html', {'productos': Producto.objects.all()})
            
            if tipo not in ['ENTRADA', 'SALIDA']:
                messages.error(request, 'Tipo inválido')
                return render(request, 'inventario/movimiento_form.html', {'productos': Producto.objects.all()})
            
            producto = get_object_or_404(Producto, id=int(producto_id))
            cantidad_int = int(cantidad)
            
            # Validar que no quede negativo en salida
            if tipo == 'SALIDA' and (producto.stock - cantidad_int) < 0:
                messages.error(request, f'Stock insuficiente. Stock actual: {producto.stock}')
                return render(request, 'inventario/movimiento_form.html', {'productos': Producto.objects.all()})
            
            # Crear movimiento
            Inventario.objects.create(
                producto=producto,
                tipo=tipo,
                cantidad=cantidad_int,
                numero_referencia=numero_referencia if numero_referencia else None
            )
            
            messages.success(request, f'{tipo}: {cantidad} unidades de {producto.nombre}')
            return redirect('inventario_dashboard')
        except (ValueError, Producto.DoesNotExist):
            messages.error(request, 'Error al procesar el movimiento')
            return render(request, 'inventario/movimiento_form.html', {'productos': Producto.objects.all()})
    
    productos = Producto.objects.all()
    return render(request, 'inventario/movimiento_form.html', {'productos': productos})