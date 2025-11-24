#!/usr/bin/env python
"""
Script para probar el envío de facturas por email
Simula el envío de una factura a un cliente
"""

import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytienda.settings')
django.setup()

from ventas.models import Venta
from ventas.views import enviar_factura_email

print("=" * 70)
print("🧪 PRUEBA DE ENVÍO DE FACTURAS POR EMAIL")
print("=" * 70)

# Obtener la última venta
venta = Venta.objects.last()

if not venta:
    print("❌ No hay ventas registradas")
    exit(1)

print(f"\n📋 Información de la venta:")
print(f"   ID: {venta.id}")
print(f"   Fecha: {venta.fecha}")
print(f"   Total: ${venta.total_final}")
print(f"   Email cliente: {venta.email_cliente or 'No especificado'}")
print(f"   Email de backup (cajero): {venta.usuario.email}")

print(f"\n📧 Configuración de email:")
print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")

print(f"\n🚀 Enviando factura...")
print("=" * 70)

resultado = enviar_factura_email(venta)

print("=" * 70)
if resultado:
    print("✅ FACTURA ENVIADA EXITOSAMENTE")
else:
    print("❌ ERROR AL ENVIAR FACTURA")
    print("\n💡 POSIBLES SOLUCIONES:")
    print("   1. Verifica que el email del cliente sea válido")
    print("   2. Verifica las credenciales de SMTP en settings.py")
    print("   3. Si usas Gmail, revisa el archivo EMAIL_CONFIGURATION.md")
    print("   4. Revisa la consola del servidor para más detalles")

print("=" * 70)
