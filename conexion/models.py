"""
Modelos de datos para MySQL
"""

from conexion.conexion import get_db_connection
from datetime import datetime
import hashlib

class Usuario:
    def __init__(self, id_usuario=None, nombre=None, mail=None, password=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.mail = mail
        self.password = password
        self.fecha_registro = None
        self.activo = True
    
    @staticmethod
    def hash_password(password):
        """Generar hash de la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create(self):
        """Crear nuevo usuario"""
        db = get_db_connection()
        hashed_password = self.hash_password(self.password)
        
        query = """
        INSERT INTO usuarios (nombre, mail, password) 
        VALUES (%s, %s, %s)
        """
        
        self.id_usuario = db.execute_insert(query, (self.nombre, self.mail, hashed_password))
        return self.id_usuario is not None
    
    @staticmethod
    def get_by_id(id_usuario):
        """Obtener usuario por ID"""
        db = get_db_connection()
        query = "SELECT * FROM usuarios WHERE id_usuario = %s"
        result = db.execute_query(query, (id_usuario,))
        
        if result:
            user_data = result[0]
            return Usuario(
                id_usuario=user_data['id_usuario'],
                nombre=user_data['nombre'],
                mail=user_data['mail'],
                password=user_data['password']
            )
        return None
    
    @staticmethod
    def get_by_mail(mail):
        """Obtener usuario por email"""
        db = get_db_connection()
        query = "SELECT * FROM usuarios WHERE mail = %s"
        result = db.execute_query(query, (mail,))
        
        if result:
            user_data = result[0]
            return Usuario(
                id_usuario=user_data['id_usuario'],
                nombre=user_data['nombre'],
                mail=user_data['mail'],
                password=user_data['password']
            )
        return None
    
    @staticmethod
    def get_all():
        """Obtener todos los usuarios"""
        db = get_db_connection()
        query = "SELECT * FROM usuarios ORDER BY nombre"
        return db.execute_query(query)
    
    def update(self):
        """Actualizar usuario"""
        db = get_db_connection()
        query = """
        UPDATE usuarios 
        SET nombre = %s, mail = %s, activo = %s 
        WHERE id_usuario = %s
        """
        
        affected = db.execute_update(query, (self.nombre, self.mail, self.activo, self.id_usuario))
        return affected > 0
    
    def delete(self):
        """Eliminar usuario"""
        db = get_db_connection()
        query = "DELETE FROM usuarios WHERE id_usuario = %s"
        affected = db.execute_update(query, (self.id_usuario,))
        return affected > 0
    
    def verify_password(self, password):
        """Verificar contraseña"""
        hashed_password = self.hash_password(password)
        return hashed_password == self.password

class ProductoMySQL:
    def __init__(self, id_producto=None, nombre=None, autor=None, categoria=None, 
                 isbn=None, cantidad=None, precio=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.autor = autor
        self.categoria = categoria
        self.isbn = isbn
        self.cantidad = cantidad
        self.precio = precio
        self.fecha_creacion = None
        self.fecha_actualizacion = None
        self.activo = True
    
    def create(self):
        """Crear nuevo producto"""
        db = get_db_connection()
        
        query = """
        INSERT INTO productos (nombre, autor, categoria, isbn, cantidad, precio) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        self.id_producto = db.execute_insert(query, (
            self.nombre, self.autor, self.categoria, 
            self.isbn, self.cantidad, self.precio
        ))
        return self.id_producto is not None
    
    @staticmethod
    def get_by_id(id_producto):
        """Obtener producto por ID"""
        db = get_db_connection()
        query = "SELECT * FROM productos WHERE id_producto = %s"
        result = db.execute_query(query, (id_producto,))
        
        if result:
            product_data = result[0]
            return ProductoMySQL(
                id_producto=product_data['id_producto'],
                nombre=product_data['nombre'],
                autor=product_data['autor'],
                categoria=product_data['categoria'],
                isbn=product_data['isbn'],
                cantidad=product_data['cantidad'],
                precio=float(product_data['precio'])
            )
        return None
    
    @staticmethod
    def get_all():
        """Obtener todos los productos"""
        db = get_db_connection()
        query = "SELECT * FROM productos WHERE activo = TRUE ORDER BY nombre"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_categoria(categoria):
        """Obtener productos por categoría"""
        db = get_db_connection()
        query = "SELECT * FROM productos WHERE categoria = %s AND activo = TRUE ORDER BY nombre"
        return db.execute_query(query, (categoria,))
    
    def update(self):
        """Actualizar producto"""
        db = get_db_connection()
        query = """
        UPDATE productos 
        SET nombre = %s, autor = %s, categoria = %s, isbn = %s, 
            cantidad = %s, precio = %s 
        WHERE id_producto = %s
        """
        
        affected = db.execute_update(query, (
            self.nombre, self.autor, self.categoria, self.isbn, 
            self.cantidad, self.precio, self.id_producto
        ))
        return affected > 0
    
    def delete(self):
        """Eliminar producto (marcar como inactivo)"""
        db = get_db_connection()
        query = "UPDATE productos SET activo = FALSE WHERE id_producto = %s"
        affected = db.execute_update(query, (self.id_producto,))
        return affected > 0
    
    @staticmethod
    def search(term):
        """Buscar productos"""
        db = get_db_connection()
        query = """
        SELECT * FROM productos 
        WHERE (nombre LIKE %s OR autor LIKE %s OR categoria LIKE %s) 
        AND activo = TRUE 
        ORDER BY nombre
        """
        search_term = f"%{term}%"
        return db.execute_query(query, (search_term, search_term, search_term))

class Categoria:
    def __init__(self, id_categoria=None, nombre=None, descripcion=None):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_creacion = None
    
    def create(self):
        """Crear nueva categoría"""
        db = get_db_connection()
        
        query = """
        INSERT INTO categorias (nombre, descripcion) 
        VALUES (%s, %s)
        """
        
        self.id_categoria = db.execute_insert(query, (self.nombre, self.descripcion))
        return self.id_categoria is not None
    
    @staticmethod
    def get_all():
        """Obtener todas las categorías"""
        db = get_db_connection()
        query = "SELECT * FROM categorias ORDER BY nombre"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_id(id_categoria):
        """Obtener categoría por ID"""
        db = get_db_connection()
        query = "SELECT * FROM categorias WHERE id_categoria = %s"
        result = db.execute_query(query, (id_categoria,))
        
        if result:
            cat_data = result[0]
            return Categoria(
                id_categoria=cat_data['id_categoria'],
                nombre=cat_data['nombre'],
                descripcion=cat_data['descripcion']
            )
        return None

class Prestamo:
    def __init__(self, id_prestamo=None, id_usuario=None, id_producto=None, 
                 fecha_prestamo=None, fecha_devolucion=None, estado='activo'):
        self.id_prestamo = id_prestamo
        self.id_usuario = id_usuario
        self.id_producto = id_producto
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado
    
    def create(self):
        """Crear nuevo préstamo"""
        db = get_db_connection()
        
        query = """
        INSERT INTO prestamos (id_usuario, id_producto, estado) 
        VALUES (%s, %s, %s)
        """
        
        self.id_prestamo = db.execute_insert(query, (self.id_usuario, self.id_producto, self.estado))
        return self.id_prestamo is not None
    
    @staticmethod
    def get_by_usuario(id_usuario):
        """Obtener préstamos de un usuario"""
        db = get_db_connection()
        query = """
        SELECT p.*, pr.nombre as producto_nombre 
        FROM prestamos p
        JOIN productos pr ON p.id_producto = pr.id_producto
        WHERE p.id_usuario = %s
        ORDER BY p.fecha_prestamo DESC
        """
        return db.execute_query(query, (id_usuario,))
    
    @staticmethod
    def get_activos():
        """Obtener préstamos activos"""
        db = get_db_connection()
        query = """
        SELECT p.*, u.nombre as usuario_nombre, pr.nombre as producto_nombre 
        FROM prestamos p
        JOIN usuarios u ON p.id_usuario = u.id_usuario
        JOIN productos pr ON p.id_producto = pr.id_producto
        WHERE p.estado = 'activo'
        ORDER BY p.fecha_prestamo DESC
        """
        return db.execute_query(query)
    
    def devolver(self):
        """Devolver producto"""
        db = get_db_connection()
        query = """
        UPDATE prestamos 
        SET estado = 'devuelto', fecha_devolucion = NOW() 
        WHERE id_prestamo = %s
        """
        
        affected = db.execute_update(query, (self.id_prestamo,))
        return affected > 0
