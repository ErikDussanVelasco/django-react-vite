from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal

from inventario.models import Producto, Proveedor, Inventario, OrdenCompra
from .models import Compra, DetalleCompra


# ==================== API PARA AUTOCOMPLETADO ====================

def api_productos(request):
    """API para obtener productos con búsqueda"""
    query = request.GET.get('q', '').lower()
    
    productos = Producto.objects.all()
    
    if query:
        productos = productos.filter(nombre__icontains=query) | productos.filter(codigo__icontains=query)
    
    productos = productos[:20]  # Limitar a 20 resultados
    
    data = [
        {
            'id': p.id,
            'nombre': p.nombre,
            'codigo': p.codigo,
            'precio_compra': str(p.precio_compra),
            'precio_venta': str(p.precio_venta),
            'stock': p.stock
        }
        for p in productos
    ]
    
    return JsonResponse(data, safe=False)


# ==================== LISTA DE COMPRAS ====================

@login_required(login_url='login')
def compra_lista(request):
    """Mostrar todas las compras registradas"""
    compras = Compra.objects.all().order_by('-id')
    return render(request, 'compras/compra_lista.html', {'compras': compras})


# ==================== CREAR COMPRA ====================

@login_required(login_url='login')
def compra_crear(request):
    """Crear nueva compra con múltiples productos"""
    proveedores = Proveedor.objects.all()
    productos = Producto.objects.all()

    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        
        if not proveedor_id:
            messages.error(request, "Debes seleccionar un proveedor.")
            return redirect('compra_crear')

        items = []
        total_compra = Decimal("0")

        # Obtener listas de datos
        producto_ids = request.POST.getlist('producto_id[]')
        cantidades = request.POST.getlist('cantidad[]')
        precios = request.POST.getlist('precio_unitario[]')

        # Procesar cada producto
        for prod_id, cantidad_str, precio_str in zip(producto_ids, cantidades, precios):
            try:
                cantidad_str = cantidad_str.strip()
                precio_str = precio_str.strip()

                if not cantidad_str or not precio_str:
                    continue

                producto = Producto.objects.get(id=prod_id)
                cantidad = int(cantidad_str)
                precio = Decimal(precio_str)

                if cantidad <= 0:
                    continue

                subtotal = cantidad * precio
                items.append((producto, cantidad, precio, subtotal))
                total_compra += subtotal

            except (Producto.DoesNotExist, ValueError):
                continue

        if not items:
            messages.error(request, "Debes agregar al menos un producto.")
            return redirect('compra_crear')

        # Crear compra
        compra = Compra.objects.create(
            proveedor_id=proveedor_id,
            total=total_compra
        )

        # Crear detalles y movimientos de inventario
        for producto, cantidad, precio_unitario, subtotal in items:
            # Detalle de compra
            DetalleCompra.objects.create(
                compra=compra,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )

            # Movimiento de inventario (ENTRADA)
            Inventario.objects.create(
                producto=producto,
                tipo="ENTRADA",
                cantidad=cantidad,
                numero_referencia=f"COMPRA-{compra.id}-{producto.id}"
            )

            # Crear orden de compra asociada
            OrdenCompra.objects.create(
                proveedor_id=proveedor_id,
                producto=producto,
                cantidad=cantidad,
                costo_unitario=precio_unitario,
                subtotal=subtotal,
                estado="RECIBIDA"
            )

        messages.success(request, f"Compra #{compra.id} registrada correctamente. Total: ${compra.total}")
        return redirect('compra_detalle', compra_id=compra.id)

    return render(request, 'compras/compra_form.html', {
        'proveedores': proveedores,
        'productos': productos
    })


# ==================== DETALLE DE COMPRA ====================

@login_required(login_url='login')
def compra_detalle(request, compra_id):
    """Ver detalles de una compra específica"""
    compra = get_object_or_404(Compra, id=compra_id)
    return render(request, 'compras/compra_detalle.html', {'compra': compra})
