"""
Configuración de conexión a MySQL para el proyecto Flask
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class MySQLConnection:
    def __init__(self):
        self.connection = None
        self.config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': os.getenv('MYSQL_DATABASE', 'biblioteca'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'autocommit': True,
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci'
        }
    
    def connect(self):
        """Establecer conexión a MySQL"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print(f"OK: Conectado exitosamente a MySQL - Base de datos: {self.config['database']}")
                return True
        except Error as e:
            print(f"ERROR: Error al conectar a MySQL: {e}")
            return False
        return False
    
    def disconnect(self):
        """Cerrar conexión a MySQL"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("OK: Conexión a MySQL cerrada")
    
    def execute_query(self, query, params=None):
        """Ejecutar consulta SQL (SELECT)"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"ERROR: Error en consulta: {e}")
        return None
    
    def execute_insert(self, query, params=None):
        """Ejecutar consulta de inserción (INSERT)"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except Error as e:
            print(f"ERROR: Error en inserción: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """Ejecutar consulta de actualización (UPDATE, DELETE)"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        except Error as e:
            print(f"ERROR: Error en actualización: {e}")
            return 0
    
    def create_tables(self):
        """Crear todas las tablas necesarias"""
        tables_created = []
        
        # Tabla de usuarios
        usuarios_sql = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            mail VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            activo BOOLEAN DEFAULT TRUE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        # Tabla de productos
        productos_sql = """
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            autor VARCHAR(255),
            categoria VARCHAR(100),
            isbn VARCHAR(20) UNIQUE,
            cantidad INT DEFAULT 0,
            precio DECIMAL(10,2) DEFAULT 0.00,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            activo BOOLEAN DEFAULT TRUE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        # Tabla de categorías
        categorias_sql = """
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) UNIQUE NOT NULL,
            descripcion TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        # Tabla de préstamos
        prestamos_sql = """
        CREATE TABLE IF NOT EXISTS prestamos (
            id_prestamo INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NOT NULL,
            id_producto INT NOT NULL,
            fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_devolucion TIMESTAMP NULL,
            estado ENUM('activo', 'devuelto', 'vencido') DEFAULT 'activo',
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
            FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        # Tabla de reservas
        reservas_sql = """
        CREATE TABLE IF NOT EXISTS reservas (
            id_reserva INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NOT NULL,
            id_producto INT NOT NULL,
            fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_expiracion TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL 7 DAY),
            estado ENUM('activa', 'cancelada', 'completada') DEFAULT 'activa',
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
            FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        tables = [
            ("usuarios", usuarios_sql),
            ("categorias", categorias_sql),
            ("productos", productos_sql),
            ("prestamos", prestamos_sql),
            ("reservas", reservas_sql)
        ]
        
        for table_name, sql in tables:
            try:
                cursor = self.connection.cursor()
                cursor.execute(sql)
                cursor.close()
                tables_created.append(table_name)
                print(f"✅ Tabla '{table_name}' creada o verificada exitosamente")
            except Error as e:
                print(f"❌ Error creando tabla '{table_name}': {e}")
        
        return tables_created
    
    def insert_sample_data(self):
        """Insertar datos de ejemplo"""
        try:
            # Insertar categorías
            categorias = [
                ("Programación", "Libros sobre lenguajes de programación y desarrollo"),
                ("Matemáticas", "Libros de matemáticas y ciencias exactas"),
                ("Literatura", "Obras literarias clásicas y contemporáneas"),
                ("Física", "Libros de física y ciencias naturales"),
                ("Negocios", "Libros sobre administración y negocios")
            ]
            
            cursor = self.connection.cursor()
            for nombre, descripcion in categorias:
                cursor.execute(
                    "INSERT IGNORE INTO categorias (nombre, descripcion) VALUES (%s, %s)",
                    (nombre, descripcion)
                )
            
            # Insertar productos
            productos = [
                ("Programación en Python", "Juan Pérez", "Programación", "978-1234567890", 15, 45.99),
                ("Cálculo Diferencial", "María González", "Matemáticas", "978-0987654321", 10, 38.75),
                ("Cien Años de Soledad", "Gabriel García Márquez", "Literatura", "978-1122334455", 8, 25.50),
                ("Física Cuántica", "Ana Martínez", "Física", "978-5566778899", 5, 67.80),
                ("Administración Moderna", "Carlos Rodríguez", "Negocios", "978-9988776655", 12, 52.30)
            ]
            
            for nombre, autor, categoria, isbn, cantidad, precio in productos:
                cursor.execute(
                    "INSERT IGNORE INTO productos (nombre, autor, categoria, isbn, cantidad, precio) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nombre, autor, categoria, isbn, cantidad, precio)
                )
            
            # Insertar usuario de ejemplo
            cursor.execute(
                "INSERT IGNORE INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
                ("Administrador", "admin@biblioteca.com", "admin123")
            )
            
            cursor.close()
            print("✅ Datos de ejemplo insertados exitosamente")
            return True
            
        except Error as e:
            print(f"❌ Error insertando datos de ejemplo: {e}")
            return False

# Instancia global de la conexión
db_connection = MySQLConnection()

def get_db_connection():
    """Obtener conexión a la base de datos"""
    if not db_connection.connection or not db_connection.connection.is_connected():
        db_connection.connect()
    return db_connection
