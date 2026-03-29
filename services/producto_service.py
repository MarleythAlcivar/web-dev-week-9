"""
Servicios de negocio para el sistema CRUD
"""

from models.producto import Producto

class ProductoService:
    """Servicio de lógica de negocio para productos"""
    
    @staticmethod
    def get_all_products():
        """Obtener todos los productos con validación"""
        try:
            productos = Producto.get_all()
            return {
                'success': True,
                'data': productos,
                'message': 'Productos obtenidos exitosamente'
            }
        except Exception as e:
            return {
                'success': False,
                'data': [],
                'message': f'Error al obtener productos: {str(e)}'
            }
    
    @staticmethod
    def get_product_by_id(id_producto):
        """Obtener producto por ID con validación"""
        try:
            if not id_producto or id_producto <= 0:
                return {
                    'success': False,
                    'data': None,
                    'message': 'ID de producto inválido'
                }
            
            producto = Producto.get_by_id(id_producto)
            if not producto:
                return {
                    'success': False,
                    'data': None,
                    'message': 'Producto no encontrado'
                }
            
            return {
                'success': True,
                'data': producto,
                'message': 'Producto encontrado exitosamente'
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Error al obtener producto: {str(e)}'
            }
    
    @staticmethod
    def search_products(term):
        """Buscar productos con validación"""
        try:
            if not term or len(term.strip()) < 2:
                return {
                    'success': False,
                    'data': [],
                    'message': 'El término de búsqueda debe tener al menos 2 caracteres'
                }
            
            productos = Producto.search(term.strip())
            return {
                'success': True,
                'data': productos,
                'message': f'Se encontraron {len(productos)} productos'
            }
        except Exception as e:
            return {
                'success': False,
                'data': [],
                'message': f'Error al buscar productos: {str(e)}'
            }
    
    @staticmethod
    def get_products_by_category(categoria):
        """Obtener productos por categoría con validación"""
        try:
            if not categoria or len(categoria.strip()) == 0:
                return {
                    'success': False,
                    'data': [],
                    'message': 'Categoría no válida'
                }
            
            productos = Producto.get_by_categoria(categoria.strip())
            return {
                'success': True,
                'data': productos,
                'message': f'Se encontraron {len(productos)} productos en {categoria}'
            }
        except Exception as e:
            return {
                'success': False,
                'data': [],
                'message': f'Error al obtener productos por categoría: {str(e)}'
            }
    
    @staticmethod
    def create_product(nombre, descripcion, precio, stock, categoria):
        """Crear nuevo producto con validación"""
        try:
            # Validaciones de negocio
            if not nombre or len(nombre.strip()) < 3:
                return {
                    'success': False,
                    'data': None,
                    'message': 'El nombre debe tener al menos 3 caracteres'
                }
            
            if not descripcion or len(descripcion.strip()) < 10:
                return {
                    'success': False,
                    'data': None,
                    'message': 'La descripción debe tener al menos 10 caracteres'
                }
            
            if not precio or float(precio) <= 0:
                return {
                    'success': False,
                    'data': None,
                    'message': 'El precio debe ser mayor que 0'
                }
            
            if not stock or int(stock) < 0:
                return {
                    'success': False,
                    'data': None,
                    'message': 'El stock no puede ser negativo'
                }
            
            # Crear producto
            producto = Producto(
                nombre=nombre.strip(),
                descripcion=descripcion.strip(),
                precio=float(precio),
                stock=int(stock),
                categoria=categoria.strip() if categoria else None
            )
            
            id_producto = producto.create()
            if id_producto:
                return {
                    'success': True,
                    'data': {'id_producto': id_producto},
                    'message': 'Producto creado exitosamente'
                }
            else:
                return {
                    'success': False,
                    'data': None,
                    'message': 'Error al crear el producto'
                }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Error al crear producto: {str(e)}'
            }
    
    @staticmethod
    def update_product(id_producto, nombre, descripcion, precio, stock, categoria, activo=True):
        """Actualizar producto existente con validación"""
        try:
            # Validaciones de negocio
            if not id_producto or id_producto <= 0:
                return {
                    'success': False,
                    'data': None,
                    'message': 'ID de producto inválido'
                }
            
            # Verificar que el producto existe
            producto_existente = Producto.get_by_id(id_producto)
            if not producto_existente:
                return {
                    'success': False,
                    'data': None,
                    'message': 'Producto no encontrado'
                }
            
            # Validar datos
            if not nombre or len(nombre.strip()) < 3:
                return {
                    'success': False,
                    'data': None,
                    'message': 'El nombre debe tener al menos 3 caracteres'
                }
            
            if not descripcion or len(descripcion.strip()) < 10:
                return {
                    'success': False,
                    'data': None,
                    'message': 'La descripción debe tener al menos 10 caracteres'
                }
            
            if not precio or float(precio) <= 0:
                return {
                    'success': False,
                    'data': None,
                    'message': 'El precio debe ser mayor que 0'
                }
            
            if not stock or int(stock) < 0:
                return {
                    'success': False,
                    'data': None,
                    'message': 'El stock no puede ser negativo'
                }
            
            # Actualizar producto
            producto = Producto(
                id_producto=id_producto,
                nombre=nombre.strip(),
                descripcion=descripcion.strip(),
                precio=float(precio),
                stock=int(stock),
                categoria=categoria.strip() if categoria else None,
                activo=activo
            )
            
            rows_affected = producto.update()
            if rows_affected > 0:
                return {
                    'success': True,
                    'data': {'rows_affected': rows_affected},
                    'message': 'Producto actualizado exitosamente'
                }
            else:
                return {
                    'success': False,
                    'data': None,
                    'message': 'No se realizaron cambios en el producto'
                }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Error al actualizar producto: {str(e)}'
            }
    
    @staticmethod
    def delete_product(id_producto, permanent=False):
        """Eliminar producto con validación"""
        try:
            if not id_producto or id_producto <= 0:
                return {
                    'success': False,
                    'message': 'ID de producto inválido'
                }
            
            # Verificar que el producto existe
            producto = Producto.get_by_id(id_producto)
            if not producto:
                return {
                    'success': False,
                    'message': 'Producto no encontrado'
                }
            
            # Eliminar producto
            producto_obj = Producto(id_producto=id_producto)
            
            if permanent:
                rows_affected = producto_obj.delete_permanent()
                action = 'eliminado permanentemente'
            else:
                rows_affected = producto_obj.delete()
                action = 'desactivado'
            
            if rows_affected > 0:
                return {
                    'success': True,
                    'message': f'Producto {action} exitosamente'
                }
            else:
                return {
                    'success': False,
                    'message': 'Error al eliminar el producto'
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al eliminar producto: {str(e)}'
            }
    
    @staticmethod
    def get_categories():
        """Obtener todas las categorías"""
        try:
            categorias = Producto.get_categories()
            return {
                'success': True,
                'data': categorias,
                'message': 'Categorías obtenidas exitosamente'
            }
        except Exception as e:
            return {
                'success': False,
                'data': [],
                'message': f'Error al obtener categorías: {str(e)}'
            }
    
    @staticmethod
    def get_low_stock_products(limit=10):
        """Obtener productos con bajo stock"""
        try:
            productos = Producto.get_low_stock(limit)
            return {
                'success': True,
                'data': productos,
                'message': f'Se encontraron {len(productos)} productos con bajo stock'
            }
        except Exception as e:
            return {
                'success': False,
                'data': [],
                'message': f'Error al obtener productos con bajo stock: {str(e)}'
            }
    
    @staticmethod
    def get_statistics():
        """Obtener estadísticas del sistema"""
        try:
            stats = Producto.get_statistics()
            return {
                'success': True,
                'data': stats,
                'message': 'Estadísticas obtenidas exitosamente'
            }
        except Exception as e:
            return {
                'success': False,
                'data': {},
                'message': f'Error al obtener estadísticas: {str(e)}'
            }
    
    @staticmethod
    def update_stock(id_producto, cantidad):
        """Actualizar stock de producto con validación"""
        try:
            if not id_producto or id_producto <= 0:
                return {
                    'success': False,
                    'message': 'ID de producto inválido'
                }
            
            if cantidad is None or int(cantidad) < 0:
                return {
                    'success': False,
                    'message': 'La cantidad de stock no puede ser negativa'
                }
            
            # Verificar que el producto existe
            producto = Producto.get_by_id(id_producto)
            if not producto:
                return {
                    'success': False,
                    'message': 'Producto no encontrado'
                }
            
            # Actualizar stock
            producto_obj = Producto(id_producto=id_producto)
            rows_affected = producto_obj.update_stock(int(cantidad))
            
            if rows_affected > 0:
                return {
                    'success': True,
                    'message': f'Stock actualizado a {cantidad} unidades'
                }
            else:
                return {
                    'success': False,
                    'message': 'No se pudo actualizar el stock'
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al actualizar stock: {str(e)}'
            }
