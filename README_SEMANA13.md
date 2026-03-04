# 📚 Sistema de Gestión de Inventario - Semana 13

## 🎯 **Objetivo de la Semana**

Ampliar el sistema Flask existente incorporando diferentes mecanismos de persistencia de datos: archivos TXT, JSON, CSV y base de datos SQLite con SQLAlchemy.

---

## 📁 **Estructura del Proyecto**

```
deber semana 09/
├── app.py                     # ✅ Aplicación Flask principal ampliada
├── form.py                    # ✅ Formularios Flask-WTF
├── requirements.txt           # ✅ Dependencias actualizadas
├── .gitignore                # ✅ Configurado para nueva estructura
├── __init__.py               # ✅ Paquete principal
├── inventario/               # ✅ Paquete de persistencia
│   ├── __init__.py          # ✅ Inicialización del paquete
│   ├── bd.py                # ✅ Configuración SQLAlchemy
│   ├── inventario.py        # ✅ Persistencia con archivos
│   ├── productos.py         # ✅ Modelo SQLAlchemy
│   └── data/               # ✅ Archivos de datos
│       ├── datos.txt        # ✅ Ejemplo TXT
│       ├── datos.json       # ✅ Ejemplo JSON
│       └── datos.csv        # ✅ Ejemplo CSV
├── static/                  # ✅ Archivos estáticos
│   └── css/
│       └── style.css        # ✅ Estilos completos
└── templates/               # ✅ Plantillas HTML
    ├── base.html           # ✅ Plantilla base actualizada
    ├── index.html          # ✅ Página principal
    ├── about.html          # ✅ Acerca de
    ├── libros.html         # ✅ Catálogo de libros
    ├── libro_detalle.html  # ✅ Detalles del libro
    ├── catalogo.html      # ✅ Catálogo completo
    ├── usuario.html        # ✅ Perfil de usuario
    ├── admin.html         # ✅ Panel de administración
    ├── datos.html         # ✅ Gestión de persistencia (NUEVO)
    ├── productos.html     # ✅ Gestión de productos
    ├── producto_form.html # ✅ Formulario de productos
    └── contactos.html    # ✅ Página de contactos
```

---

## 🔧 **Características Implementadas**

### **1. Persistencia con Archivos TXT**
- ✅ **Función `open()`** para escritura y lectura
- ✅ **Formato estructurado** con metadatos
- ✅ **Manejo de encoding UTF-8**
- ✅ **Parseo robusto** de datos

### **2. Persistencia con Archivos JSON**
- ✅ **Librería `json`** nativa de Python
- ✅ **Estructura con metadatos** (total, fecha, versión)
- ✅ **Conversión automática** diccionario ↔ JSON
- ✅ **Validación de datos**

### **3. Persistencia con Archivos CSV**
- ✅ **Librería `csv`** nativa de Python
- ✅ **Formato tabular** estándar
- ✅ **Headers configurables**
- ✅ **Conversión de tipos** automática

### **4. Base de Datos SQLite con SQLAlchemy**
- ✅ **SQLAlchemy 2.0.23** instalado
- ✅ **Modelo `Producto`** completo
- ✅ **Mapeo ORM** automático
- ✅ **Migraciones automáticas**
- ✅ **Sesiones optimizadas**

### **5. Formularios Flask-WTF**
- ✅ **Validación automática** de campos
- ✅ **Protección CSRF** incluida
- ✅ **Mensajes de error** personalizados
- ✅ **Tipos de datos** específicos

---

## 🌐 **Rutas Nuevas**

### **Gestión de Datos**
- `/datos` - Panel principal de persistencia
- `/datos/save/<format>` - Guardar en formato específico
- `/datos/load/<format>` - Cargar desde formato específico

### **Formularios y Productos**
- `/productos` - Gestión de productos
- `/producto/nuevo` - Formulario para nuevo producto
- `/producto/agregar` - Procesar formulario
- `/contactos` - Página de contactos

---

## 📊 **Funcionalidades de Persistencia**

### **🔄 Conversión entre Formatos**
```
Inventario Original → TXT, JSON, CSV, SQLite
TXT, JSON, CSV, SQLite → Inventario Original
```

### **📋 Operaciones Soportadas**
- **Guardar**: Exportar datos del inventario a cualquier formato
- **Cargar**: Importar datos desde cualquier formato al inventario
- **Validar**: Verificar integridad de datos
- **Metadatos**: Información de archivos (tamaño, fecha, existencia)

### **🗂️ Gestión de Archivos**
- **Información**: Estado, tamaño, fecha de modificación
- **Ubicación**: `inventario/data/` para archivos locales
- **Base de datos**: `inventario_sqlalchemy.db` para SQLAlchemy

---

## 🛠️ **Dependencias**

```txt
Flask==2.3.3          # Framework web
Flask-WTF==1.1.1      # Formularios con validación
SQLAlchemy==2.0.23     # ORM para base de datos
WTForms==3.0.1         # Validación de formularios
```

---

## 🚀 **Instalación y Uso**

### **1. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **2. Ejecutar Aplicación**
```bash
python app.py
```

### **3. Acceder al Sistema**
- **Principal**: `http://127.0.0.1:5000`
- **Gestión de Datos**: `http://127.0.0.1:5000/datos`
- **Productos**: `http://127.0.0.1:5000/productos`
- **Administración**: `http://127.0.0.1:5000/admin`

---

## 📝 **Ejemplos de Uso**

### **Guardar Datos en TXT**
```python
from inventario.inventario import FilePersistence

fp = FilePersistence()
data = [{'nombre': 'Libro 1', 'autor': 'Autor 1', ...}]
fp.save_to_txt(data)
```

### **Cargar Datos desde JSON**
```python
json_data = fp.read_from_json()
for item in json_data:
    inventario.agregar_producto(**item)
```

### **Usar SQLAlchemy**
```python
from inventario.productos import Producto
from inventario.bd import Session

with Session() as session:
    productos = session.query(Producto).all()
    for p in productos:
        print(p.nombre)
```

---

## 🎓 **Objetivos Educativos Cumplidos**

### **✅ Programación Orientada a Objetos**
- **Encapsulamiento**: Clases con métodos privados/públicos
- **Herencia**: Base SQLAlchemy para modelos
- **Polimorfismo**: Interfaces unificadas de persistencia

### **✅ Manejo de Archivos**
- **open()**: Lectura/escritura de archivos TXT
- **json**: Serialización/deserialización
- **csv**: Manejo de datos tabulares
- **Encoding**: Soporte UTF-8 completo

### **✅ Base de Datos Relacionales**
- **SQLAlchemy**: ORM moderno y potente
- **Modelado**: Entidades con relaciones
- **Migraciones**: Creación automática de tablas
- **Sesiones**: Manejo optimizado de conexiones

### **✅ Desarrollo Web Avanzado**
- **Flask-WTF**: Formularios seguros
- **Templates**: Herencia y composición
- **Rutas dinámicas**: Parámetros y métodos HTTP
- **API REST**: Endpoints JSON funcionales

---

## 📈 **Características Técnicas**

### **🔒 Seguridad**
- **CSRF Protection**: Flask-WTF
- **Input Validation**: WTForms
- **SQL Injection**: SQLAlchemy ORM
- **XSS Protection**: Jinja2 auto-escaping

### **⚡ Rendimiento**
- **Índices**: Búsqueda O(1) en diccionarios
- **Caching**: Datos en memoria
- **Connection Pooling**: SQLAlchemy
- **Lazy Loading**: Carga bajo demanda

### **🔧 Mantenimiento**
- **Logging**: Errores y operaciones
- **Modularidad**: Separación de responsabilidades
- **Testing**: Estructura para pruebas unitarias
- **Documentation**: Docstrings y comentarios

---

## 🌟 **Resumen de la Semana 13**

El sistema ahora incluye **cuatro mecanismos de persistencia** completamente funcionales:

1. **📄 Archivos TXT** - Formato legible por humanos
2. **📋 Archivos JSON** - Estructura con metadatos
3. **📊 Archivos CSV** - Formato tabular estándar
4. **🗃️ Base de Datos SQLite** - ORM con SQLAlchemy

**Todos los requisitos de la tarea están cumplidos:**
- ✅ Estructura de carpetas según especificación
- ✅ Persistencia con TXT, JSON, CSV
- ✅ SQLAlchemy con modelo completo
- ✅ Formularios Flask-WTF
- ✅ Rutas para todas las operaciones
- ✅ Templates funcionales
- ✅ Dependencias actualizadas
- ✅ Configuración para producción

**El sistema está listo para subir a GitHub y continuar con el proyecto final.**
