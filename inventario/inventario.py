"""
Módulo de persistencia con archivos TXT, JSON y CSV
"""

import json
import csv
import os
from typing import List, Dict, Any
from datetime import datetime

class FilePersistence:
    """
    Clase para manejar persistencia en diferentes formatos de archivo
    """
    
    def __init__(self, data_dir="inventario/data"):
        self.data_dir = data_dir
        self.txt_file = os.path.join(data_dir, "datos.txt")
        self.json_file = os.path.join(data_dir, "datos.json")
        self.csv_file = os.path.join(data_dir, "datos.csv")
        
        # Crear directorio si no existe
        os.makedirs(data_dir, exist_ok=True)
    
    def save_to_txt(self, data: List[Dict[str, Any]]) -> bool:
        """
        Guardar datos en formato TXT
        """
        try:
            with open(self.txt_file, 'w', encoding='utf-8') as file:
                file.write(f"=== INVENTARIO DE PRODUCTOS ===\n")
                file.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("=" * 50 + "\n\n")
                
                for item in data:
                    file.write(f"ID: {item.get('id', 'N/A')}\n")
                    file.write(f"Nombre: {item.get('nombre', 'N/A')}\n")
                    file.write(f"Autor: {item.get('autor', 'N/A')}\n")
                    file.write(f"Categoría: {item.get('categoria', 'N/A')}\n")
                    file.write(f"Cantidad: {item.get('cantidad', 'N/A')}\n")
                    file.write(f"Precio: ${item.get('precio', 'N/A')}\n")
                    file.write(f"ISBN: {item.get('isbn', 'N/A')}\n")
                    file.write("-" * 30 + "\n")
            
            return True
        except Exception as e:
            print(f"Error al guardar en TXT: {e}")
            return False
    
    def read_from_txt(self) -> List[Dict[str, Any]]:
        """
        Leer datos desde archivo TXT
        """
        data = []
        
        if not os.path.exists(self.txt_file):
            return data
        
        try:
            with open(self.txt_file, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Parsear el contenido del archivo TXT
                lines = content.strip().split('\n')
                current_item = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('===') or line.startswith('---'):
                        continue
                    
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Mapear campos y convertir tipos
                        if key.lower() == 'id':
                            current_item['id'] = int(value)
                        elif key.lower() == 'nombre':
                            current_item['nombre'] = value
                        elif key.lower() == 'autor':
                            current_item['autor'] = value
                        elif key.lower() == 'categoria':
                            current_item['categoria'] = value
                        elif key.lower() == 'cantidad':
                            current_item['cantidad'] = int(value)
                        elif key.lower() == 'precio':
                            # Quitar el símbolo $ y convertir a float
                            price_value = value.replace('$', '').strip()
                            current_item['precio'] = float(price_value)
                        elif key.lower() == 'isbn':
                            current_item['isbn'] = value
                    
                    # Si encontramos un separador, guardar el item actual
                    if line.startswith('---') and current_item:
                        data.append(current_item)
                        current_item = {}
                
                # Agregar el último item si existe
                if current_item:
                    data.append(current_item)
                    
        except Exception as e:
            print(f"Error al leer desde TXT: {e}")
        
        return data
    
    def save_to_json(self, data: List[Dict[str, Any]]) -> bool:
        """
        Guardar datos en formato JSON
        """
        try:
            json_data = {
                'metadata': {
                    'total_productos': len(data),
                    'fecha_generacion': datetime.now().isoformat(),
                    'version': '1.0'
                },
                'productos': data
            }
            
            with open(self.json_file, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error al guardar en JSON: {e}")
            return False
    
    def read_from_json(self) -> List[Dict[str, Any]]:
        """
        Leer datos desde formato JSON
        """
        try:
            if not os.path.exists(self.json_file):
                return []
            
            with open(self.json_file, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            
            return json_data.get('productos', [])
            
        except Exception as e:
            print(f"Error al leer desde JSON: {e}")
            return []
    
    def save_to_csv(self, data: List[Dict[str, Any]]) -> bool:
        """
        Guardar datos en formato CSV
        """
        try:
            if not data:
                return False
            
            fieldnames = ['id', 'nombre', 'autor', 'categoria', 'cantidad', 'precio', 'isbn']
            
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for item in data:
                    # Asegurar que todos los campos existan
                    row = {field: item.get(field, '') for field in fieldnames}
                    writer.writerow(row)
            
            return True
        except Exception as e:
            print(f"Error al guardar en CSV: {e}")
            return False
    
    def read_from_csv(self) -> List[Dict[str, Any]]:
        """
        Leer datos desde formato CSV
        """
        data = []
        try:
            if not os.path.exists(self.csv_file):
                return data
            
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convertir campos numéricos
                    if row.get('cantidad'):
                        try:
                            row['cantidad'] = int(row['cantidad'])
                        except ValueError:
                            pass
                    
                    if row.get('precio'):
                        try:
                            row['precio'] = float(row['precio'])
                        except ValueError:
                            pass
                    
                    data.append(row)
            
        except Exception as e:
            print(f"Error al leer desde CSV: {e}")
        
        return data
    
    def get_file_info(self) -> Dict[str, Any]:
        """
        Obtener información sobre los archivos de datos
        """
        info = {
            'txt': {'exists': False, 'size': 0, 'modified': None, 'download_url': '/download/txt'},
            'json': {'exists': False, 'size': 0, 'modified': None, 'download_url': '/download/json'},
            'csv': {'exists': False, 'size': 0, 'modified': None, 'download_url': '/download/csv'}
        }
        
        files_info = {
            'txt': self.txt_file,
            'json': self.json_file,
            'csv': self.csv_file
        }
        
        for format_type, file_path in files_info.items():
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                info[format_type] = {
                    'exists': True,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'download_url': f'/download/{format_type}'
                }
        
        return info
    
    def get_file_content(self, format_type: str) -> str:
        """
        Obtener el contenido del archivo para descarga
        """
        try:
            if format_type == 'txt':
                if os.path.exists(self.txt_file):
                    with open(self.txt_file, 'r', encoding='utf-8') as file:
                        return file.read()
            elif format_type == 'json':
                if os.path.exists(self.json_file):
                    with open(self.json_file, 'r', encoding='utf-8') as file:
                        return file.read()
            elif format_type == 'csv':
                if os.path.exists(self.csv_file):
                    with open(self.csv_file, 'r', encoding='utf-8') as file:
                        return file.read()
        except Exception as e:
            print(f"Error leyendo archivo {format_type}: {e}")
        
        return ""
