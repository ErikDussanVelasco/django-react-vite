#!/usr/bin/env python
"""
Script para probar la configuración de email
Ejecutar: python manage.py shell < test_email.py
O simplemente: python test_email.py
"""

import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytienda.settings')
django.setup()

from django.core.mail import send_mail, EmailMessage

print("=" * 60)
print("🧪 PRUEBA DE CONFIGURACIÓN DE EMAIL")
print("=" * 60)

# Mostrar configuración actual
print("\n📋 CONFIGURACIÓN ACTUAL:")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

print("\n" + "=" * 60)
print("🚀 INTENTANDO ENVIAR EMAIL DE PRUEBA...")
print("=" * 60)

try:
    # Intentar enviar un email simple
    asunto = "🧪 Prueba de Configuración - Stock Master"
    cuerpo = """
Este es un email de prueba para verificar que la configuración de email funciona correctamente.

Si recibiste este email, significa que tu configuración SMTP está correcta.

Stock Master Test
    """
    
    email = EmailMessage(
        subject=asunto,
        body=cuerpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.EMAIL_HOST_USER],  # Enviar a la misma cuenta para test
    )
    
    resultado = email.send()
    
    if resultado:
        print(f"✅ EMAIL ENVIADO EXITOSAMENTE")
        print(f"   De: {settings.DEFAULT_FROM_EMAIL}")
        print(f"   Para: {settings.EMAIL_HOST_USER}")
    else:
        print(f"❌ EMAIL NO SE ENVIÓ (send() retornó 0)")
        
except Exception as e:
    print(f"❌ ERROR AL ENVIAR EMAIL:")
    print(f"   Tipo de error: {type(e).__name__}")
    print(f"   Mensaje: {str(e)}")
    print(f"\n💡 POSIBLES SOLUCIONES:")
    print(f"   1. Verifica que EMAIL_HOST_USER y EMAIL_HOST_PASSWORD sean correctos")
    print(f"   2. Si usas Gmail, genera una contraseña de aplicación:")
    print(f"      https://myaccount.google.com/apppasswords")
    print(f"   3. Verifica que EMAIL_HOST y EMAIL_PORT sean correctos")
    print(f"   4. Asegúrate de que EMAIL_USE_TLS = True")

print("\n" + "=" * 60)
print("✅ PRUEBA COMPLETADA")
print("=" * 60)
