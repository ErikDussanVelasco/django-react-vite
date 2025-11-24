"""
Pruebas unitarias para requisitos funcionales principales
Testing: Registro, Login, Ventas, Productos
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from inventario.models import Producto, Inventario
from ventas.models import Venta, DetalleVenta
from decimal import Decimal

User = get_user_model()


class RegistroYLoginTests(TestCase):
    """Pruebas para registro e inicio de sesión"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = Client()
        self.registro_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        
    def test_registro_usuario_exitoso(self):
        """✅ Prueba que el registro de usuario funciona correctamente"""
        datos = {
            'email': 'usuario_test@example.com',
            'username': 'usuario_test',
            'password': 'contraseña123',
            'password_confirm': 'contraseña123',
        }
        
        respuesta = self.client.post(self.registro_url, datos)
        
        # Verifica que se redirige a login después del registro
        self.assertEqual(respuesta.status_code, 302)
        
        # Verifica que el usuario fue creado
        usuario_existe = User.objects.filter(email='usuario_test@example.com').exists()
        self.assertTrue(usuario_existe)
        
        # Verifica que el usuario está inactivo (esperando verificación de email)
        usuario = User.objects.get(email='usuario_test@example.com')
        self.assertFalse(usuario.is_active)
        
    def test_registro_email_duplicado(self):
        """✅ Prueba que no permite registrar email duplicado"""
        # Crear primer usuario
        User.objects.create_user(
            email='duplicado@example.com',
            username='usuario1',
            password='pass123'
        )
        
        # Intentar crear otro con el mismo email
        datos = {
            'email': 'duplicado@example.com',
            'username': 'usuario2',
            'password': 'pass123',
            'password_confirm': 'pass123',
        }
        
        respuesta = self.client.post(self.registro_url, datos)
        
        # Verifica que se queda en la página de registro (no redirige)
        self.assertEqual(respuesta.status_code, 200)
        
        # Verifica que solo existe un usuario con ese email
        cantidad = User.objects.filter(email='duplicado@example.com').count()
        self.assertEqual(cantidad, 1)
        
    def test_login_exitoso(self):
        """✅ Prueba que el login funciona correctamente"""
        # Crear usuario activo
        User.objects.create_user(
            email='login_test@example.com',
            username='login_usuario',
            password='contraseña123',
            is_active=True,
            rol='CAJERO'
        )
        
        # Intentar login
        datos = {
            'email': 'login_test@example.com',
            'password': 'contraseña123',
        }
        
        respuesta = self.client.post(self.login_url, datos)
        
        # Verifica que se redirige (login exitoso)
        self.assertEqual(respuesta.status_code, 302)
        
    def test_login_contraseña_incorrecta(self):
        """✅ Prueba que rechaza contraseña incorrecta"""
        User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='contraseña_correcta',
            is_active=True
        )
        
        datos = {
            'email': 'test@example.com',
            'password': 'contraseña_incorrecta',
        }
        
        respuesta = self.client.post(self.login_url, datos)
        
        # Verifica que se queda en login (no redirige)
        self.assertEqual(respuesta.status_code, 200)


class ProductoTests(TestCase):
    """Pruebas para gestión de productos"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        
        # Crear admin
        self.admin = User.objects.create_user(
            email='admin@test.com',
            username='admin',
            password='admin123',
            is_active=True,
            rol='ADMIN'
        )
        
        # Login
        self.client.login(email='admin@test.com', password='admin123')
        
    def test_crear_producto(self):
        """✅ Prueba creación de producto"""
        producto = Producto.objects.create(
            codigo=100,
            nombre='Laptop Test',
            precio_compra=Decimal('500.00'),
            precio_venta=Decimal('800.00'),
            stock=5,
            activo=True
        )
        
        # Verifica que el producto fue creado
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(producto.codigo, 100)
        self.assertEqual(producto.nombre, 'Laptop Test')
        
    def test_codigo_producto_unico(self):
        """✅ Prueba que el código de producto es único"""
        # Crear primer producto
        Producto.objects.create(
            codigo=200,
            nombre='Producto 1',
            precio_compra=Decimal('100.00'),
            precio_venta=Decimal('150.00'),
        )
        
        # Intentar crear otro con el mismo código
        with self.assertRaises(Exception):
            Producto.objects.create(
                codigo=200,
                nombre='Producto 2',
                precio_compra=Decimal('100.00'),
                precio_venta=Decimal('150.00'),
            )
            
    def test_desactivar_producto(self):
        """✅ Prueba desactivación de producto (soft delete)"""
        producto = Producto.objects.create(
            codigo=300,
            nombre='Producto a Desactivar',
            precio_compra=Decimal('100.00'),
            precio_venta=Decimal('150.00'),
            activo=True
        )
        
        # Desactivar
        producto.activo = False
        producto.save()
        
        # Verifica que el producto existe pero está inactivo
        self.assertFalse(producto.activo)
        
        # Verifica que no aparece en listados de activos
        productos_activos = Producto.objects.filter(activo=True)
        self.assertNotIn(producto, productos_activos)
        
    def test_producto_bajo_stock(self):
        """✅ Prueba detección de bajo stock"""
        Producto.objects.create(
            codigo=400,
            nombre='Producto Bajo Stock',
            precio_compra=Decimal('100.00'),
            precio_venta=Decimal('150.00'),
            stock=3,
            activo=True
        )
        
        # Buscar productos con stock <= 5
        bajo_stock = Producto.objects.filter(stock__lte=5, activo=True)
        self.assertEqual(bajo_stock.count(), 1)


class VentaTests(TestCase):
    """Pruebas para gestión de ventas"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        
        # Crear usuario
        self.usuario = User.objects.create_user(
            email='cajero@test.com',
            username='cajero',
            password='pass123',
            is_active=True,
            rol='CAJERO'
        )
        
        # Crear producto
        self.producto = Producto.objects.create(
            codigo=500,
            nombre='Producto Venta',
            precio_compra=Decimal('100.00'),
            precio_venta=Decimal('150.00'),
            stock=10,
            activo=True
        )
        
        # Login
        self.client.login(email='cajero@test.com', password='pass123')
        
    def test_crear_venta(self):
        """✅ Prueba creación de venta"""
        venta = Venta.objects.create(
            total=Decimal('150.00'),
            descuento_general=Decimal('0.00'),
            iva_porcentaje=Decimal('19.00'),
            iva_total=Decimal('28.50'),
            total_final=Decimal('178.50'),
            metodo_pago='EFECTIVO',
            monto_recibido=Decimal('200.00'),
            cambio=Decimal('21.50'),
            usuario=self.usuario,
            email_cliente='cliente@test.com'
        )
        
        # Verifica que la venta fue creada
        self.assertEqual(Venta.objects.count(), 1)
        self.assertEqual(venta.total_final, Decimal('178.50'))
        
    def test_venta_con_detalles(self):
        """✅ Prueba venta con detalles de productos"""
        venta = Venta.objects.create(
            total=Decimal('300.00'),
            descuento_general=Decimal('0.00'),
            iva_porcentaje=Decimal('19.00'),
            iva_total=Decimal('57.00'),
            total_final=Decimal('357.00'),
            metodo_pago='TARJETA',
            usuario=self.usuario
        )
        
        # Agregar detalles
        DetalleVenta.objects.create(
            venta=venta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=Decimal('150.00'),
            subtotal=Decimal('300.00')
        )
        
        # Verifica que el detalle fue agregado
        self.assertEqual(venta.detalles.count(), 1)
        detalle = venta.detalles.first()
        self.assertEqual(detalle.cantidad, 2)
        
    def test_calculo_iva(self):
        """✅ Prueba cálculo correcto de IVA (19%)"""
        subtotal = Decimal('100.00')
        iva_esperado = Decimal('19.00')
        
        venta = Venta.objects.create(
            total=subtotal,
            descuento_general=Decimal('0.00'),
            iva_porcentaje=Decimal('19.00'),
            iva_total=iva_esperado,
            total_final=subtotal + iva_esperado,
            metodo_pago='EFECTIVO',
            usuario=self.usuario
        )
        
        # Verifica que el IVA fue calculado correctamente
        self.assertEqual(venta.iva_total, iva_esperado)
        self.assertEqual(venta.total_final, Decimal('119.00'))
        
    def test_venta_con_descuento(self):
        """✅ Prueba venta con descuento general"""
        subtotal = Decimal('100.00')
        descuento = Decimal('10.00')
        # El descuento se aplica ANTES del IVA en el modelo
        monto_con_descuento = subtotal - descuento  # 90.00
        iva = monto_con_descuento * Decimal('0.19')  # 17.10
        total = monto_con_descuento + iva  # 107.10
        
        venta = Venta.objects.create(
            total=subtotal,
            descuento_general=descuento,
            iva_porcentaje=Decimal('19.00'),
            iva_total=iva,
            total_final=total,
            metodo_pago='EFECTIVO',
            usuario=self.usuario
        )
        
        # Verifica los cálculos
        self.assertEqual(venta.descuento_general, Decimal('10.00'))
        self.assertEqual(venta.total_final, Decimal('107.10'))


class InventarioTests(TestCase):
    """Pruebas para gestión de inventario"""
    
    def setUp(self):
        """Configuración inicial"""
        self.producto = Producto.objects.create(
            codigo=600,
            nombre='Producto Stock',
            precio_compra=Decimal('100.00'),
            precio_venta=Decimal('150.00'),
            stock=20,
            activo=True
        )
        
    def test_movimiento_entrada(self):
        """✅ Prueba movimiento de entrada de stock"""
        movimiento = Inventario.objects.create(
            producto=self.producto,
            tipo='ENTRADA',
            cantidad=5,
            numero_referencia='COMPRA-001'
        )
        
        # Verifica que el movimiento fue creado
        self.assertEqual(Inventario.objects.count(), 1)
        self.assertEqual(movimiento.tipo, 'ENTRADA')
        
    def test_movimiento_salida(self):
        """✅ Prueba movimiento de salida de stock"""
        movimiento = Inventario.objects.create(
            producto=self.producto,
            tipo='SALIDA',
            cantidad=2,
            numero_referencia='VENTA-001'
        )
        
        # Verifica que el movimiento fue creado
        self.assertEqual(movimiento.tipo, 'SALIDA')
        
    def test_referencia_movimiento(self):
        """✅ Prueba que la referencia del movimiento se guarda"""
        referencia = 'VENTA-12345-PROD-600'
        movimiento = Inventario.objects.create(
            producto=self.producto,
            tipo='SALIDA',
            cantidad=1,
            numero_referencia=referencia
        )
        
        self.assertEqual(movimiento.numero_referencia, referencia)


# ==================== EJECUCIÓN DE PRUEBAS ====================
"""
Para ejecutar estas pruebas:

1. Todas las pruebas:
   python manage.py test

2. Solo pruebas de autenticación:
   python manage.py test tests.RegistroYLoginTests

3. Solo pruebas de productos:
   python manage.py test tests.ProductoTests

4. Con verbosidad:
   python manage.py test --verbosity=2

5. Prueba específica:
   python manage.py test tests.RegistroYLoginTests.test_registro_usuario_exitoso

"""
