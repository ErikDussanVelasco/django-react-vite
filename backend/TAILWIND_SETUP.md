# 🎨 Configuración de Tailwind CSS en Django

## ✅ Instalación Completada

Tailwind CSS ya está completamente integrado en tu proyecto Django.

## 📦 Dependencias Instaladas

```bash
✓ django-tailwind==3.9.0
✓ pytailwindcss==0.3.0
```

## ⚙️ Configuración en `settings.py`

Se agregó `'tailwind'` a `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',  # ← Agregado
    'rest_framework',
    'corsheaders',
    'inventario',
    'accounts'
]
```

## 📁 Estructura de Archivos

```
backend/
├── static/
│   └── css/
│       └── style.css          # CSS personalizado
├── tailwind.config.js         # Configuración de Tailwind
├── tailwind.config.full.js    # Configuración extendida
└── templates/
    ├── inventario/
    │   ├── base.html
    │   ├── dashboard.html
    │   ├── producto_lista.html
    │   ├── producto_form.html
    │   └── movimiento_form.html
    └── accounts/
```

## 🚀 Cómo Usar Tailwind en Templates

Todos los templates ya incluyen Tailwind automáticamente a través del CDN:

```html
<script src="https://cdn.tailwindcss.com"></script>
```

### Ejemplo de Uso:

```html
<div class="bg-white rounded-xl shadow-lg p-8">
    <h1 class="text-3xl font-bold text-gray-800">Título</h1>
    <p class="text-gray-600">Descripción</p>
    
    <button class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg transition">
        Click me
    </button>
</div>
```

## 📝 Clases Tailwind Personalizadas

Se agregaron colores personalizados en `tailwind.config.js`:

```css
--primary-color: #0e2a47     (Azul oscuro)
--secondary-color: #1b3e63   (Azul secundario)
```

Úsalos en tus templates:

```html
<div class="bg-[#0e2a47] text-white">
    Fondo azul oscuro
</div>
```

## 🎯 Clases Tailwind Comúnmente Usadas

### Colores
- `bg-gray-100`, `bg-blue-500`, `bg-green-600`
- `text-gray-800`, `text-white`
- `border-gray-300`

### Espaciado
- `px-4` (padding horizontal)
- `py-2` (padding vertical)
- `p-6` (padding all)
- `m-4` (margin)
- `gap-6` (grid gap)

### Tamaño de Fuente
- `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-3xl`
- `font-light`, `font-normal`, `font-semibold`, `font-bold`

### Bordes y Sombras
- `rounded`, `rounded-lg`, `rounded-xl`
- `shadow`, `shadow-lg`, `shadow-2xl`
- `border`, `border-2`

### Display y Layout
- `flex`, `grid`, `block`, `inline-block`, `hidden`
- `grid-cols-1`, `md:grid-cols-2`, `lg:grid-cols-3`
- `gap-4`, `gap-6`, `gap-8`

### Transiciones
- `transition` (añade animación suave)
- `hover:bg-blue-600` (cambio en hover)
- `focus:ring-2 focus:ring-blue-500`

## 🔄 Responsive Design

Tailwind usa prefijos de breakpoint:

```html
<!-- Extra pequeño (por defecto) -->
<div class="w-full">

<!-- Pequeño (sm: 640px) -->
<div class="sm:w-1/2">

<!-- Mediano (md: 768px) -->
<div class="md:w-1/3">

<!-- Grande (lg: 1024px) -->
<div class="lg:w-1/4">

<!-- Extra grande (xl: 1280px) -->
<div class="xl:w-1/6">
```

Ejemplo:
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <!-- 1 columna en móvil, 2 en tablet, 4 en desktop -->
</div>
```

## 🎨 Ejemplos de Componentes

### Botón
```html
<button class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-lg transition">
    Click
</button>
```

### Card
```html
<div class="bg-white rounded-xl shadow-lg p-8">
    <h2 class="text-2xl font-bold text-gray-800">Título</h2>
    <p class="text-gray-600 mt-2">Contenido</p>
</div>
```

### Input
```html
<input 
    type="text" 
    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    placeholder="Escribe algo..."
>
```

### Grid
```html
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <div class="bg-white rounded-lg p-6">Item 1</div>
    <div class="bg-white rounded-lg p-6">Item 2</div>
    <div class="bg-white rounded-lg p-6">Item 3</div>
</div>
```

## 🚀 Ejecutar el Proyecto

```bash
# 1. Navega a la carpeta backend
cd backend

# 2. Instala las dependencias
pip install -r ../requirements.txt

# 3. Migra la BD
python manage.py migrate

# 4. Inicia el servidor
python manage.py runserver

# 5. Abre en el navegador
http://localhost:8000/
```

## 📚 Recursos Oficiales

- **Documentación Tailwind:** https://tailwindcss.com/docs
- **Configuración:** https://tailwindcss.com/docs/configuration
- **Ejemplos:** https://tailwindui.com/

## ✨ Características Implementadas

✅ Tailwind CSS integrado con CDN  
✅ Colores personalizados  
✅ Responsive design (mobile-first)  
✅ Componentes estilizados  
✅ Transiciones suaves  
✅ Modo oscuro compatible  

## 🐛 Solución de Problemas

### Los estilos no se aplican
1. Abre la consola (F12)
2. Verifica que no haya errores de CORS
3. Asegúrate de usar clases válidas de Tailwind

### Las clases no funcionan
1. Comprueba la sintaxis: `class="flex gap-4 p-6"`
2. Usa comillas: `class="..."` no `class='...'`
3. No espacios en los nombres: `grid-cols-1` no `grid-cols-1 `

### Necesito más personalización
Edita `tailwind.config.js` para agregar tus propias clases:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        'mi-color': '#ff0000',
      },
    },
  },
}
```

---

**Última actualización:** 13 de Noviembre, 2025  
**Versión:** 1.0  
**Estado:** ✅ Listo para usar
