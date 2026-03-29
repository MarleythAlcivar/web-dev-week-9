"""
Modelos de datos para el sistema CRUD
"""

from conexion.conexion import get_db_connection

class Producto:
    """Modelo de Producto para el sistema CRUD"""
    
    def __init__(self, id_producto=None, nombre=None, descripcion=None, precio=None, stock=None, categoria=None, activo=True):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.activo = activo
    
    @staticmethod
    def get_all():
        """Obtener todos los productos activos"""
        db = get_db_connection()
        query = """
        SELECT id_producto, nombre, descripcion, precio, stock, categoria, activo
        FROM productos 
        WHERE activo = TRUE 
        ORDER BY nombre
        """
        return db.execute_query(query)
    
    @staticmethod
    def get_by_id(id_producto):
        """Obtener producto por ID"""
        db = get_db_connection()
        query = """
        SELECT id_producto, nombre, descripcion, precio, stock, categoria, activo
        FROM productos 
        WHERE id_producto = %s AND activo = TRUE
        """
        result = db.execute_query(query, (id_producto,))
        return result[0] if result else None
    
    @staticmethod
    def get_by_categoria(categoria):
        """Obtener productos por categoría"""
        db = get_db_connection()
        query = """
        SELECT id_producto, nombre, descripcion, precio, stock, categoria, activo
        FROM productos 
        WHERE categoria = %s AND activo = TRUE 
        ORDER BY nombre
        """
        return db.execute_query(query, (categoria,))
    
    @staticmethod
    def search(term):
        """Buscar productos por nombre o descripción"""
        db = get_db_connection()
        query = """
        SELECT id_producto, nombre, descripcion, precio, stock, categoria, activo
        FROM productos 
        WHERE (nombre LIKE %s OR descripcion LIKE %s) AND activo = TRUE 
        ORDER BY nombre
        """
        search_term = f"%{term}%"
        return db.execute_query(query, (search_term, search_term))
    
    def create(self):
        """Crear nuevo producto"""
        db = get_db_connection()
        query = """
        INSERT INTO productos (nombre, descripcion, precio, stock, categoria, activo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (self.nombre, self.descripcion, self.precio, self.stock, self.categoria, self.activo)
        return db.execute_insert(query, params)
    
    def update(self):
        """Actualizar producto existente"""
        db = get_db_connection()
        query = """
        UPDATE productos 
        SET nombre = %s, descripcion = %s, precio = %s, stock = %s, categoria = %s, activo = %s
        WHERE id_producto = %s
        """
        params = (self.nombre, self.descripcion, self.precio, self.stock, self.categoria, self.activo, self.id_producto)
        return db.execute_update(query, params)
    
    def delete(self):
        """Eliminar producto (borrado lógico)"""
        db = get_db_connection()
        query = "UPDATE productos SET activo = FALSE WHERE id_producto = %s"
        return db.execute_update(query, (self.id_producto,))
    
    def delete_permanent(self):
        """Eliminar producto permanentemente"""
        db = get_db_connection()
        query = "DELETE FROM productos WHERE id_producto = %s"
        return db.execute_update(query, (self.id_producto,))
    
    def update_stock(self, cantidad):
        """Actualizar stock del producto"""
        db = get_db_connection()
        query = "UPDATE productos SET stock = %s WHERE id_producto = %s"
        return db.execute_update(query, (cantidad, self.id_producto))
    
    def get_stock(self):
        """Obtener stock actual del producto"""
        db = get_db_connection()
        query = "SELECT stock FROM productos WHERE id_producto = %s"
        result = db.execute_query(query, (self.id_producto,))
        return result[0]['stock'] if result else 0
    
    @staticmethod
    def get_categories():
        """Obtener todas las categorías de productos"""
        db = get_db_connection()
        query = """
        SELECT DISTINCT categoria 
        FROM productos 
        WHERE categoria IS NOT NULL AND activo = TRUE 
        ORDER BY categoria
        """
        result = db.execute_query(query)
        return [row['categoria'] for row in result]
    
    @staticmethod
    def get_low_stock(limit=10):
        """Obtener productos con bajo stock"""
        db = get_db_connection()
        query = """
        SELECT id_producto, nombre, descripcion, precio, stock, categoria, activo
        FROM productos 
        WHERE stock <= 10 AND activo = TRUE 
        ORDER BY stock ASC 
        LIMIT %s
        """
        return db.execute_query(query, (limit,))
    
    @staticmethod
    def get_statistics():
        """Obtener estadísticas de productos"""
        db = get_db_connection()
        
        # Total de productos
        total_query = "SELECT COUNT(*) as total FROM productos WHERE activo = TRUE"
        total_result = db.execute_query(total_query)
        total = total_result[0]['total'] if total_result else 0
        
        # Valor total del inventario
        value_query = "SELECT SUM(precio * stock) as total_value FROM productos WHERE activo = TRUE"
        value_result = db.execute_query(value_query)
        total_value = value_result[0]['total_value'] if value_result and value_result[0]['total_value'] else 0
        
        # Productos con bajo stock
        low_stock_query = "SELECT COUNT(*) as low_stock FROM productos WHERE stock <= 10 AND activo = TRUE"
        low_stock_result = db.execute_query(low_stock_query)
        low_stock = low_stock_result[0]['low_stock'] if low_stock_result else 0
        
        return {
            'total_products': total,
            'total_value': total_value,
            'low_stock_products': low_stock,
            'categories_count': len(Producto.get_categories())
        }
    
    def to_dict(self):
        """Convertir producto a diccionario"""
        return {
            'id_producto': self.id_producto,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'categoria': self.categoria,
            'activo': self.activo
        }
