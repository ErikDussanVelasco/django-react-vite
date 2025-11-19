# 📦 Sistema de Inventario - Documentación

## Descripción General
Sistema completo de gestión de inventario con API REST y vistas HTML.

---

## 🏗️ Estructura de Datos

### Producto
```python
- codigo (int): Código único del producto
- nombre (str): Nombre del producto
- stock (int): Cantidad en stock (se actualiza automáticamente)
- precio_compra (decimal): Precio de costo
- precio_venta (decimal): Precio de venta
```

### Inventario (Movimientos)
```python
- producto (FK): Referencia al producto
- tipo (str): ENTRADA o SALIDA
- cantidad (int): Cantidad del movimiento
- numero_referencia (str): Referencia (OC, factura, etc)
```

---

## 📍 Rutas Disponibles

### VISTAS HTML (Template)
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/inventario/` | GET | Dashboard principal |
| `/inventario/productos/` | GET | Lista de productos |
| `/inventario/productos/crear/` | GET/POST | Crear nuevo producto |
| `/inventario/movimientos/` | GET/POST | Registrar entrada/salida |

### API REST
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/inventario/api/productos/` | GET | Listar todos los productos |
| `/inventario/api/productos/` | POST | Crear producto (API) |
| `/inventario/api/productos/{id}/` | GET | Obtener producto específico |
| `/inventario/api/productos/{id}/` | PUT | Actualizar producto |
| `/inventario/api/productos/{id}/` | DELETE | Eliminar producto |
| `/inventario/api/movimientos/` | GET | Listar movimientos |
| `/inventario/api/movimientos/` | POST | Crear movimiento (API) |
| `/inventario/api/movimientos/{id}/` | GET | Obtener movimiento |

---

## ✨ Características Principales

### 1. Dashboard
- Resumen de estadísticas (total productos, stock total)
- Últimos 10 movimientos registrados
- Acceso rápido a funciones principales

### 2. Gestión de Productos
- Crear productos con código, nombre, precios
- Ver lista completa con stock actualizado
- Validación de códigos únicos
- Cálculo automático de ganancia (precio_venta - precio_compra)

### 3. Movimientos de Inventario
- Registrar ENTRADAS (compras, devoluciones)
- Registrar SALIDAS (ventas, pérdidas)
- Número de referencia opcional (OC, factura, etc)
- Prevención automática de stock negativo en salidas
- Actualización automática del stock del producto

### 4. Seguridad
- Todas las vistas requieren autenticación (@login_required)
- Validaciones en servidor
- Manejo de excepciones robusto

---

## 🔄 Flujo de Trabajo

### Crear Producto
```
1. Ir a /inventario/productos/crear/
2. Llenar formulario (código, nombre, precios)
3. Hacer clic en "Crear Producto"
4. Stock inicial = 0
```

### Registrar Entrada
```
1. Ir a /inventario/movimientos/
2. Seleccionar producto
3. Seleccionar "ENTRADA"
4. Ingresa cantidad
5. Clic en "Registrar Movimiento"
6. Stock del producto se incrementa
```

### Registrar Salida
```
1. Ir a /inventario/movimientos/
2. Seleccionar producto
3. Seleccionar "SALIDA"
4. Ingresa cantidad
5. Sistema valida que hay stock suficiente
6. Clic en "Registrar Movimiento"
7. Stock del producto se decrementa
```

---

## 🐛 Validaciones Implementadas

| Validación | Descripción |
|-----------|-------------|
| Código único | No permite duplicar códigos de producto |
| Stock no negativo | Impide salidas que dejen stock negativo |
| Campos obligatorios | Valida que todos los campos requeridos se completen |
| Tipos válidos | Solo acepta ENTRADA o SALIDA |
| Números válidos | Valida que códigos y precios sean números |

---

## 📊 Vistas Disponibles en HTML

### Dashboard (`/inventario/`)
```
- 3 tarjetas con estadísticas
- 2 botones de acción (Nuevo Producto, Nuevo Movimiento)
- Tabla con últimos 10 movimientos
- Indicadores de color (verde=entrada, rojo=salida)
```

### Lista de Productos (`/inventario/productos/`)
```
- Tabla completa de productos
- Columnas: Código, Nombre, Stock, Precio Compra, Precio Venta, Ganancia
- Color del stock: verde (>0), rojo (0)
- Botón para crear nuevo producto
```

### Crear Producto (`/inventario/productos/crear/`)
```
- Formulario con campos: Código, Nombre, Precio Compra, Precio Venta
- Botones: Crear Producto, Cancelar
- Validaciones en tiempo real
```

### Registrar Movimiento (`/inventario/movimientos/`)
```
- Select de productos (muestra stock actual)
- Select de tipo (ENTRADA/SALIDA)
- Input de cantidad
- Input opcional de referencia
- Info box con explicación
```

---

## 🚀 Ejemplo de Uso con cURL (API REST)

### Crear Producto
```bash
curl -X POST http://localhost:8000/inventario/api/productos/ \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": 12345,
    "nombre": "Laptop Dell",
    "precio_compra": "500.00",
    "precio_venta": "750.00"
  }'
```

### Listar Productos
```bash
curl http://localhost:8000/inventario/api/productos/
```

### Registrar Entrada
```bash
curl -X POST http://localhost:8000/inventario/api/movimientos/ \
  -H "Content-Type: application/json" \
  -d '{
    "producto": 1,
    "tipo": "ENTRADA",
    "cantidad": 10,
    "numero_referencia": "OC-2025-001"
  }'
```

---

## 📝 Próximas Mejoras Sugeridas

1. **Editar Productos**: Permitir modificar productos existentes
2. **Eliminar Productos**: Con validación de movimientos
3. **Reportes**: Ganancias por periodo, productos más vendidos
4. **Búsqueda y Filtrado**: Por código, nombre, rango de stock
5. **Historial de Precios**: Rastrear cambios de precios
6. **Alertas de Stock**: Notificar cuando stock es bajo
7. **Múltiples Almacenes**: Gestionar stock en diferentes ubicaciones
8. **Usuarios Multiplos**: Rastro de quién hace cada movimiento

---

## ⚙️ Configuración

### Permisos Requeridos
- Usuario debe estar autenticado para acceder a cualquier vista

### Base de Datos
- Migraciones ya creadas en `inventario/migrations/0001_initial.py`
- Run: `python manage.py migrate`

### Dependencias
- Django 5.2.7+
- Django REST Framework 3.16.1+

---

**Última actualización:** 13 de Noviembre, 2025
