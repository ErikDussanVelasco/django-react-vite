#!/usr/bin/env python
"""
Script simple para ejecutar pruebas unitarias con Django
"""
import os
import sys
import django

# Configurar paths
backend_dir = os.path.dirname(__file__)
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytienda.settings')
django.setup()

from django.core.management import call_command

if __name__ == '__main__':
    # Ejecutar tests
    call_command('test', 'test_requisitos_funcionales', '--verbosity=2', '--keepdb')
