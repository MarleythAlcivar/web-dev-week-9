#!/usr/bin/env python3
"""
Script para generar reporte PDF de demostración sin conexión a base de datos
"""

from reports.pdf_generator import PDFGenerator
from datetime import datetime
import os

def generar_reporte_demo():
    """Generar reporte PDF con datos de demostración"""
    try:
        print("Generando reporte PDF de demostración...")
        
        # Datos de demostración
        productos_demo = [
            {
                'id_producto': 1,
                'nombre': 'Laptop HP Pavilion',
                'descripcion': 'Laptop de 15.6 pulgadas, Intel i5, 8GB RAM, 256GB SSD',
                'precio': 599.99,
                'stock': 15,
                'categoria': 'Tecnología',
                'activo': True
            },
            {
                'id_producto': 2,
                'nombre': 'Mouse Inalámbrico Logitech',
                'descripcion': 'Mouse inalámbrico ergonómico con receptor USB',
                'precio': 25.99,
                'stock': 45,
                'categoria': 'Tecnología',
                'activo': True
            },
            {
                'id_producto': 3,
                'nombre': 'Teclado Mecánico RGB',
                'descripcion': 'Teclado mecánico con retroiluminación RGB',
                'precio': 79.99,
                'stock': 8,
                'categoria': 'Tecnología',
                'activo': True
            },
            {
                'id_producto': 4,
                'nombre': 'Monitor 24 pulgadas',
                'descripcion': 'Monitor LED Full HD 1080p, 75Hz',
                'precio': 189.99,
                'stock': 5,
                'categoria': 'Tecnología',
                'activo': True
            },
            {
                'id_producto': 5,
                'nombre': 'Python para Principiantes',
                'descripcion': 'Libro introductorio de programación Python',
                'precio': 29.99,
                'stock': 20,
                'categoria': 'Libros',
                'activo': True
            },
            {
                'id_producto': 6,
                'nombre': 'Silla de Oficina',
                'descripcion': 'Silla ergonómica con soporte lumbar',
                'precio': 149.99,
                'stock': 3,
                'categoria': 'Oficina',
                'activo': True
            },
            {
                'id_producto': 7,
                'nombre': 'Botella de Agua',
                'descripcion': 'Botella de acero inoxidable 500ml',
                'precio': 12.99,
                'stock': 50,
                'categoria': 'Deportes',
                'activo': True
            },
            {
                'id_producto': 8,
                'nombre': 'Cafetera de Goteo',
                'descripcion': 'Cafetera programable para 12 tazas',
                'precio': 89.99,
                'stock': 7,
                'categoria': 'Hogar',
                'activo': True
            }
        ]
        
        print(f"Se encontraron {len(productos_demo)} productos de demostración")
        
        # Generar PDF general
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_productos_demo_{timestamp}.pdf"
        
        pdf_gen = PDFGenerator(filename)
        pdf_result = pdf_gen.generate_product_report(productos_demo, "Reporte General de Productos - Demo")
        
        if pdf_result['success']:
            print(f"Reporte PDF generado exitosamente:")
            print(f"Archivo: {pdf_result['filepath']}")
            print(f"Nombre: {pdf_result['filename']}")
            print(f"Productos incluidos: {len(productos_demo)}")
            
            # Verificar que el archivo existe
            if os.path.exists(pdf_result['filepath']):
                file_size = os.path.getsize(pdf_result['filepath'])
                print(f"Tamano del archivo: {file_size} bytes")
                
                # Generar reporte de bajo stock
                productos_bajo_stock = [p for p in productos_demo if p['stock'] <= 10]
                print(f"\nGenerando reporte de bajo stock ({len(productos_bajo_stock)} productos)...")
                
                filename_bajo = f"reporte_bajo_stock_demo_{timestamp}.pdf"
                pdf_gen_bajo = PDFGenerator(filename_bajo)
                pdf_result_bajo = pdf_gen_bajo.generate_low_stock_report(productos_bajo_stock, "Reporte de Productos con Bajo Stock - Demo")
                
                if pdf_result_bajo['success']:
                    print(f"Reporte de bajo stock generado:")
                    print(f"Archivo: {pdf_result_bajo['filepath']}")
                    print(f"Nombre: {pdf_result_bajo['filename']}")
                    print(f"Productos criticos: {len(productos_bajo_stock)}")
                    
                    if os.path.exists(pdf_result_bajo['filepath']):
                        file_size_bajo = os.path.getsize(pdf_result_bajo['filepath'])
                        print(f"Tamano del archivo: {file_size_bajo} bytes")
                    
                    return True
                else:
                    print(f"Error generando PDF de bajo stock: {pdf_result_bajo['message']}")
                    return False
            else:
                print("El archivo PDF no se creo correctamente")
                return False
        else:
            print(f"Error generando PDF: {pdf_result['message']}")
            return False
    
    except Exception as e:
        print(f"Error general: {e}")
        return False

if __name__ == "__main__":
    print("Generador de Reportes PDF - Demostracion")
    print("=" * 50)
    
    # Generar reporte de demostración
    print("\nGenerando Reporte de Demostracion...")
    exito_demo = generar_reporte_demo()
    
    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN:")
    print(f"Reporte Demo: {'Generado' if exito_demo else 'Error'}")
    
    if exito_demo:
        print("\nReporte de demostracion generado exitosamente")
        print("Los archivos PDF estan en la carpeta 'reports/'")
        print("\nPara generar reportes reales:")
        print("1. Configura la base de datos MySQL")
        print("2. Ejecuta el script crear_base_datos.sql")
        print("3. Ejecuta python generar_reporte.py")
    else:
        print("\nNo se pudo generar el reporte de demostracion")
        print("Verifica la instalacion de reportlab")
