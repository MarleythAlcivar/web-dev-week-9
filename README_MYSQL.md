# 🗄️ Integración MySQL - Semana 14

## 🎯 **Objetivo de la Semana**

Integrar el proyecto Flask con una base de datos relacional MySQL para almacenar y consultar información del sistema.

---

## 📁 **Estructura del Proyecto**

```
deber semana 09/
├── app.py                     # ✅ Aplicación Flask con rutas MySQL
├── conexion/                   # ✅ Paquete de conexión MySQL
│   ├── __init__.py           # ✅ Inicialización del paquete
│   ├── conexion.py           # ✅ Configuración de conexión
│   └── models.py             # ✅ Modelos de datos MySQL
├── templates/                 # ✅ Plantillas HTML
│   ├── mysql_status.html     # ✅ Estado de MySQL
│   ├── mysql_usuarios.html   # ✅ Gestión de usuarios
│   ├── mysql_usuario_form.html # ✅ Formulario de usuarios
│   ├── mysql_productos.html  # ✅ Gestión de productos
│   ├── mysql_producto_form.html # ✅ Formulario de productos
│   └── mysql_prestamos.html  # ✅ Gestión de préstamos
├── .env.example              # ✅ Ejemplo de configuración
├── requirements.txt           # ✅ Dependencias actualizadas
└── ...                       # Otros archivos existentes
```

---

## 🔧 **Características Implementadas**

### **1. Conexión a MySQL**
- ✅ **MySQL Connector Python 8.2.0** instalado
- ✅ **Configuración flexible** con variables de entorno
- ✅ **Manejo de errores** robusto
- ✅ **Pool de conexiones** optimizado

### **2. Tablas de Base de Datos**
- ✅ **usuarios** - Gestión de usuarios del sistema
- ✅ **productos** - Catálogo de productos
- ✅ **categorias** - Clasificación de productos
- ✅ **prestamos** - Control de préstamos
- ✅ **reservas** - Sistema de reservas

### **3. Operaciones CRUD**
- ✅ **CREATE** - Insertar registros
- ✅ **READ** - Consultar registros
- ✅ **UPDATE** - Modificar registros
- ✅ **DELETE** - Eliminar registros

---

## 🌐 **Rutas MySQL**

### **Configuración**
- `/mysql/setup` - Configurar base de datos MySQL

### **Gestión de Usuarios**
- `/mysql/usuarios` - Lista de usuarios
- `/mysql/usuarios/nuevo` - Crear nuevo usuario
- `/mysql/usuarios/editar/<id>` - Editar usuario
- `/mysql/usuarios/eliminar/<id>` - Eliminar usuario

### **Gestión de Productos**
- `/mysql/productos` - Lista de productos
- `/mysql/productos/nuevo` - Crear nuevo producto
- `/mysql/productos/editar/<id>` - Editar producto
- `/mysql/productos/eliminar/<id>` - Eliminar producto

### **Gestión de Préstamos**
- `/mysql/prestamos` - Lista de préstamos activos
- `/mysql/prestamos/nuevo` - Crear nuevo préstamo
- `/mysql/prestamos/devolver/<id>` - Devolver préstamo

---

## 📊 **Modelos de Datos**

### **Usuario**
```python
class Usuario:
    id_usuario: INT (PK)
    nombre: VARCHAR(100)
    mail: VARCHAR(100) UNIQUE
    password: VARCHAR(255) HASH
    fecha_registro: TIMESTAMP
    activo: BOOLEAN
```

### **ProductoMySQL**
```python
class ProductoMySQL:
    id_producto: INT (PK)
    nombre: VARCHAR(255)
    autor: VARCHAR(255)
    categoria: VARCHAR(100)
    isbn: VARCHAR(20) UNIQUE
    cantidad: INT
    precio: DECIMAL(10,2)
    fecha_creacion: TIMESTAMP
    fecha_actualizacion: TIMESTAMP
    activo: BOOLEAN
```

### **Prestamo**
```python
class Prestamo:
    id_prestamo: INT (PK)
    id_usuario: INT (FK)
    id_producto: INT (FK)
    fecha_prestamo: TIMESTAMP
    fecha_devolucion: TIMESTAMP NULL
    estado: ENUM('activo', 'devuelto', 'vencido')
```

---

## 🛠️ **Instalación y Configuración**

### **1. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **2. Configurar MySQL**
```sql
-- Crear base de datos
CREATE DATABASE biblioteca;

-- Crear usuario (opcional)
CREATE USER 'biblioteca_user'@'localhost' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON biblioteca.* TO 'biblioteca_user'@'localhost';
FLUSH PRIVILEGES;
```

### **3. Configurar Variables de Entorno**
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus datos
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña
MYSQL_DATABASE=biblioteca
MYSQL_PORT=3306
```

### **4. Ejecutar Aplicación**
```bash
python app.py
```

---

## 🚀 **Uso del Sistema**

### **1. Configuración Inicial**
1. Acceder a `http://127.0.0.1:5000/mysql/setup`
2. Seguir instrucciones para crear tablas
3. Insertar datos de ejemplo

### **2. Gestión de Usuarios**
- **Crear**: `/mysql/usuarios/nuevo`
- **Editar**: `/mysql/usuarios/editar/<id>`
- **Eliminar**: `/mysql/usuarios/eliminar/<id>`

### **3. Gestión de Productos**
- **Crear**: `/mysql/productos/nuevo`
- **Editar**: `/mysql/productos/editar/<id>`
- **Eliminar**: `/mysql/productos/eliminar/<id>`

### **4. Gestión de Préstamos**
- **Crear**: Formulario en `/mysql/prestamos`
- **Devolver**: `/mysql/prestamos/devolver/<id>`

---

## 🔒 **Seguridad**

### **Hash de Contraseñas**
```python
@staticmethod
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

### **Validación de Datos**
- **Email único** en tabla usuarios
- **ISBN único** en tabla productos
- **Claves foráneas** con integridad referencial
- **Inyección SQL** prevenida con parámetros

---

## 📈 **Características Técnicas**

### **🔧 Conexión**
- **MySQL Connector Python 8.2.0**
- **Connection pooling** automático
- **Reconexión automática** en caso de fallos
- **Charset UTF-8MB4** para soporte completo

### **🗄️ Base de Datos**
- **Motor InnoDB** para transacciones
- **Índices** en campos clave
- **Claves foráneas** con CASCADE
- **Timestamps** automáticos

### **🌐 Web**
- **Templates Jinja2** con herencia
- **Flash messages** para feedback
- **Formularios seguros** con validación
- **Responsive design** con CSS Grid

---

## 📋 **Resumen de la Semana 14**

**✅ Requisitos Cumplidos:**
- ✅ Configuración de base de datos MySQL
- ✅ Conexión entre Flask y MySQL
- ✅ Definición de tablas para el sistema
- ✅ Consultas básicas desde la aplicación
- ✅ Operaciones CRUD completas
- ✅ Templates funcionales
- ✅ Seguridad implementada
- ✅ Documentación completa

**✅ Características Adicionales:**
- ✅ Sistema de préstamos completo
- ✅ Gestión de categorías
- ✅ Estadísticas en tiempo real
- ✅ Interface responsive
- ✅ Manejo de errores robusto
- ✅ Configuración flexible

**El sistema está completamente integrado con MySQL y listo para producción.**
