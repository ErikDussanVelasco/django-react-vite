#!/usr/bin/env python
"""
Script para ejecutar pruebas unitarias con reporte visual en tiempo real
Muestra progreso por requisito funcional con porcentajes
"""

import os
import sys
import time
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

# Configurar paths ANTES de importar Django
backend_dir = os.path.dirname(__file__)
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytienda.settings')

import django
django.setup()

from django.conf import settings
from django.test.utils import get_runner
from django.test.runner import DiscoverRunner

try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

# Colores para la consola
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Imprime encabezado"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}📋 EJECUTOR DE PRUEBAS UNITARIAS - STOCK MASTER{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.ENDC}\n")

def print_section(title):
    """Imprime sección"""
    print(f"{Colors.BOLD}{Colors.CYAN}>>> {title}{Colors.ENDC}")

def print_success(text):
    """Imprime texto exitoso"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    """Imprime error"""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(text):
    """Imprime información"""
    print(f"{Colors.YELLOW}ℹ {text}{Colors.ENDC}")


def close_test_db_connections():
    """Cierra todas las conexiones a la BD de prueba"""
    if not HAS_PSYCOPG2:
        print_info("psycopg2 no está instalado, saltando limpieza de BD...")
        return
    
    print_section("Limpiando conexiones a la base de datos...")
    
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(
            dbname='postgres',
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', ''),
            host=os.environ.get('DB_HOST', 'localhost'),
            port=os.environ.get('DB_PORT', '5432')
        )
        cursor = conn.cursor()
        
        # Terminar todas las conexiones a test_postgres
        cursor.execute("""
            SELECT pid FROM pg_stat_activity 
            WHERE datname = 'test_postgres' AND pid <> pg_backend_pid()
        """)
        
        pids = cursor.fetchall()
        for pid in pids:
            try:
                cursor.execute(f"SELECT pg_terminate_backend({pid[0]})")
                print_success(f"Conexión {pid[0]} terminada")
            except Exception as e:
                print_info(f"No se pudo terminar conexión {pid[0]}: {e}")
        
        # Intentar eliminar la BD de prueba
        try:
            cursor.execute("DROP DATABASE IF EXISTS test_postgres")
            print_success("Base de datos de prueba eliminada")
        except Exception as e:
            print_info(f"BD ya no existe o no se puede eliminar: {e}")
        
        cursor.close()
        conn.commit()
        conn.close()
        
    except Exception as e:
        print_error(f"Error al limpiar conexiones: {e}")
        print_info("Continuando de todos modos...")

def run_tests():
    """Ejecuta los tests"""
    print_section("Iniciando pruebas unitarias...")
    print()
    
    # Definir requisitos funcionales y sus clases de test
    requisitos = {
        'RF07': ('ProveedorTestsRF07', 'Gestión de Proveedores', 5),
        'RF15': ('ComprasTestsRF15', 'Compras', 4),
        'RF16': ('InventarioTestsRF16', 'Inventario', 5),
        'RF08': ('VentasTestsRF08', 'Gestión de Ventas', 5),
        'RF09': ('FacturacionTestsRF09', 'Facturación', 3),
        'RF13': ('LoginTestsRF13', 'Login', 4),
        'RF14': ('RegistroTestsRF14', 'Registro de Usuarios', 4),
        'RF10': ('UsuariosTestsRF10', 'Gestión de Usuarios', 3),
        'RF11': ('ReportesTestsRF11', 'Reportes y Consultas', 3),
        'RF12': ('DevolucionesTestsRF12', 'Devoluciones', 3),
    }
    
    total_tests = sum(count for _, _, count in requisitos.values())
    tests_passed = 0
    tests_failed = 0
    start_time = time.time()
    
    print(f"{Colors.BOLD}Total de pruebas a ejecutar: {total_tests}{Colors.ENDC}\n")
    
    # Ejecutar cada requisito
    for rf, (test_class, description, expected_count) in requisitos.items():
        test_label = f'test_requisitos_funcionales.{test_class}'
        
        print(f"\n{Colors.BOLD}{rf} - {description}{Colors.ENDC}")
        print(f"{'─' * 60}")
        
        try:
            # Ejecutar tests de este requisito
            TestRunner = get_runner(settings)
            test_runner = TestRunner(
                verbosity=1,
                keepdb=True,
                interactive=False,
                failfast=False,
            )
            
            # Capturar output
            out = StringIO()
            err = StringIO()
            
            start_rf = time.time()
            with redirect_stdout(out), redirect_stderr(err):
                failures = test_runner.run_tests([test_label])
            duration_rf = time.time() - start_rf
            
            # Procesar resultados
            if failures == 0:
                print_success(f"Todos los tests de {rf} pasaron ({expected_count}/{expected_count}) - {duration_rf:.2f}s")
                percentage = 100
                tests_passed += expected_count
            else:
                print_error(f"Fallos en {rf}: {failures} de {expected_count} tests fallaron - {duration_rf:.2f}s")
                percentage = ((expected_count - failures) / expected_count) * 100
                tests_passed += (expected_count - failures)
                tests_failed += failures
            
            print(f"Progreso: {Colors.BOLD}{percentage:.0f}%{Colors.ENDC}")
            
        except Exception as e:
            print_error(f"Error al ejecutar {rf}: {str(e)[:100]}")
            tests_failed += expected_count
    
    # Resumen final
    total_time = time.time() - start_time
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}RESUMEN FINAL{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.ENDC}\n")
    
    print(f"Total de pruebas:     {total_tests}")
    print(f"Pruebas exitosas:     {Colors.GREEN}{tests_passed}{Colors.ENDC}")
    print(f"Pruebas fallidas:     {Colors.RED}{tests_failed}{Colors.ENDC}")
    print(f"Porcentaje de éxito:  {Colors.BOLD}{(tests_passed/total_tests)*100:.1f}%{Colors.ENDC}")
    print(f"Tiempo total:         {total_time:.2f} segundos\n")
    
    if tests_failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ¡TODAS LAS PRUEBAS PASARON!{Colors.ENDC}\n")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Algunas pruebas fallaron{Colors.ENDC}\n")
        return 1

def main():
    """Función principal"""
    print_header()
    
    # Limpiar conexiones
    close_test_db_connections()
    
    print()
    time.sleep(1)
    
    # Ejecutar tests
    exit_code = run_tests()
    
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
