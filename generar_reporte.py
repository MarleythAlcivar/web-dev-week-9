#!/usr/bin/env python3
"""
Script para generar reporte PDF de productos
"""

from reports.pdf_generator import PDFGenerator
from services.producto_service import ProductoService
from datetime import datetime
import os

def generar_reporte_general():
    """Generar reporte general de productos en PDF"""
    try:
        print("Generando reporte general de productos...")
        
        # Obtener productos
        result = ProductoService.get_all_products()
        
        if not result['success']:
            print(f"Error obteniendo productos: {result['message']}")
            return False
        
        productos = result['data']
        print(f"Se encontraron {len(productos)} productos")
        
        if not productos:
            print("No hay productos para generar el reporte")
            return False
        
        # Generar PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_productos_{timestamp}.pdf"
        
        pdf_gen = PDFGenerator(filename)
        pdf_result = pdf_gen.generate_product_report(productos, "Reporte General de Productos")
        
        if pdf_result['success']:
            print(f"Reporte PDF generado exitosamente:")
            print(f"Archivo: {pdf_result['filepath']}")
            print(f"Nombre: {pdf_result['filename']}")
            print(f"Productos incluidos: {len(productos)}")
            
            # Verificar que el archivo existe
            if os.path.exists(pdf_result['filepath']):
                file_size = os.path.getsize(pdf_result['filepath'])
                print(f"Tamano del archivo: {file_size} bytes")
                return True
            else:
                print("El archivo PDF no se creo correctamente")
                return False
        else:
            print(f"Error generando PDF: {pdf_result['message']}")
            return False
    
    except Exception as e:
        print(f"Error general: {e}")
        return False

def generar_reporte_bajo_stock():
    """Generar reporte de productos con bajo stock"""
    try:
        print("Generando reporte de productos con bajo stock...")
        
        # Obtener productos con bajo stock
        result = ProductoService.get_low_stock_products()
        
        if not result['success']:
            print(f"Error obteniendo productos con bajo stock: {result['message']}")
            return False
        
        productos = result['data']
        print(f"Se encontraron {len(productos)} productos con bajo stock")
        
        if not productos:
            print("No hay productos con bajo stock")
            return True
        
        # Generar PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_bajo_stock_{timestamp}.pdf"
        
        pdf_gen = PDFGenerator(filename)
        pdf_result = pdf_gen.generate_low_stock_report(productos, "Reporte de Productos con Bajo Stock")
        
        if pdf_result['success']:
            print(f"Reporte de bajo stock generado exitosamente:")
            print(f"Archivo: {pdf_result['filepath']}")
            print(f"Nombre: {pdf_result['filename']}")
            print(f"Productos criticos: {len(productos)}")
            return True
        else:
            print(f"Error generando PDF de bajo stock: {pdf_result['message']}")
            return False
    
    except Exception as e:
        print(f"Error general: {e}")
        return False

if __name__ == "__main__":
    print("Generador de Reportes PDF - Sistema CRUD")
    print("=" * 50)
    
    # Generar reporte general
    print("\n1. Generando Reporte General...")
    exito_general = generar_reporte_general()
    
    # Generar reporte de bajo stock
    print("\n2. Generando Reporte de Bajo Stock...")
    exito_bajo_stock = generar_reporte_bajo_stock()
    
    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN:")
    print(f"Reporte General: {'Generado' if exito_general else 'Error'}")
    print(f"Reporte Bajo Stock: {'Generado' if exito_bajo_stock else 'Error'}")
    
    if exito_general or exito_bajo_stock:
        print("\nAl menos un reporte fue generado exitosamente")
        print("Los archivos PDF estan en la carpeta 'reports/'")
    else:
        print("\nNo se pudo generar ningun reporte")
        print("Verifica la conexion a la base de datos")
