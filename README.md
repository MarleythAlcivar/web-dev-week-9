# Sistema Avanzado de Gestión de Inventario - Librería Virtual

## Descripción

Este proyecto es un sistema completo de gestión de inventarios para una librería virtual, desarrollado con Flask, Programación Orientada a Objetos (POO), colecciones y base de datos SQLite. El sistema permite gestionar libros de manera eficiente con operaciones CRUD completas.

## Características Principales

### 🏗️ Arquitectura del Sistema

- **Programación Orientada a Objetos**: Clases `Producto` e `Inventario` con encapsulamiento y métodos específicos
- **Colecciones Optimizadas**: Uso eficiente de diccionarios, listas, conjuntos y tuplas para búsquedas rápidas
- **Base de Datos SQLite**: Almacenamiento persistente con conexión automática
- **API REST**: Endpoints para operaciones CRUD vía HTTP
- **Interfaz Web**: Integración con templates Flask existentes
- **Menú Interactivo**: Consola para gestión directa del inventario

### 📚 Gestión de Productos

- **Atributos del Producto**: ID, nombre, cantidad, precio, autor, categoría, ISBN, etiquetas
- **Validación de Datos**: Control de integridad en setters
- **Búsquedas Avanzadas**: Por nombre, autor, categoría, ISBN, ID
- **Índices Optimizados**: Búsqueda por substring y referencias cruzadas

### 🔧 Operaciones CRUD

- **Crear**: Agregar nuevos productos al inventario
- **Leer**: Consultar productos por diferentes criterios
- **Actualizar**: Modificar atributos de productos existentes
- **Eliminar**: Remover productos del inventario

### 📊 Estadísticas y Reportes

- **Estadísticas del Inventario**: Total de productos, valor del inventario, categorías populares
- **Control de Stock**: Alertas de productos con bajo stock
- **Exportación de Datos**: Formato de tuplas y estadísticas

## Estructura del Proyecto

```
deber semana 09/
├── app.py                 # Aplicación Flask principal con rutas web y API
├── models.py              # Clases POO: Producto e Inventario
├── menu_interactivo.py    # Interfaz de consola para gestión directa
├── requirements.txt       # Dependencias del proyecto
├── inventario.db         # Base de datos SQLite (se crea automáticamente)
├── templates/            # Templates HTML para la interfaz web
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── libros.html
│   ├── catalogo.html
│   ├── libro_detalle.html
│   └── usuario.html
├── static/               # Archivos estáticos (CSS, JS, imágenes)
└── README.md            # Este archivo
```

## Instalación y Ejecución

### Prerrequisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. Clonar o descargar el proyecto
2. Navegar al directorio del proyecto
3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

### Ejecución

#### Opción 1: Interfaz Web (Flask)

```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

#### Opción 2: Menú Interactivo (Consola)

```bash
python menu_interactivo.py
```

## Uso de Colecciones en el Sistema

### 🗂️ Diccionarios Principales

- **`_productos`**: `Dict[int, Producto]` - Almacenamiento principal por ID
- **`_categorias`**: `Dict[str, Set[int]]` - Índice de categorías
- **`_autores`**: `Dict[str, Set[int]]` - Índice de autores
- **`_isbn_index`**: `Dict[str, int]` - Índice de ISBN
- **`_nombre_index`**: `Dict[str, List[int]]` - Índice de nombres para búsqueda por substring

### 🔢 Conjuntos (Sets)

- **`_etiquetas`**: `Set[str]` - Etiquetas únicas por producto
- **Índices de categorías y autores**: `Set[int>` - IDs únicos por categoría/autor

### 📋 Listas y Tuplas

- **Resultados de búsqueda**: `List[Producto]` - Listas de productos encontrados
- **Exportación**: `List[Tuple]` - Formato de tuplas para exportación

## API REST Endpoints

### Productos

- `GET /api/productos` - Obtener todos los productos
- `POST /api/producto` - Crear nuevo producto
- `PUT /api/producto/<id>` - Actualizar producto existente
- `DELETE /api/producto/<id>` - Eliminar producto

### Búsqueda

- `GET /api/buscar?q=<termino>&tipo=<tipo>` - Buscar productos
  - `tipo`: nombre, autor, categoria, isbn

### Estadísticas

- `GET /api/estadisticas` - Obtener estadísticas del inventario

## Ejemplos de Uso

### Agregar un Producto (API)

```python
import requests

# Agregar nuevo libro
nuevo_libro = {
    "nombre": "Cien Años de Soledad",
    "cantidad": 10,
    "precio": 25.99,
    "autor": "Gabriel García Márquez",
    "categoria": "Literatura Latinoamericana",
    "isbn": "978-0307474728"
}

response = requests.post('http://localhost:5000/api/producto', json=nuevo_libro)
print(response.json())
```

### Buscar por Categoría

```python
# Buscar libros de "Ciencias Exactas"
response = requests.get('http://localhost:5000/api/buscar?q=Ciencias%20Exactas&tipo=categoria')
libros = response.json()
for libro in libros:
    print(f"{libro['nombre']} - {libro['autor']}")
```

### Uso del Menú Interactivo

1. Ejecutar `python menu_interactivo.py`
2. Seleccionar opciones del menú:
   - Opción 1: Agregar nuevo producto
   - Opción 4: Buscar producto
   - Opción 6: Ver estadísticas
   - Opción 9: Productos con bajo stock

## Validaciones y Control de Errores

### Validaciones de Datos

- **Nombre**: No puede estar vacío
- **Cantidad**: No puede ser negativa
- **Precio**: No puede ser negativo, se redondea a 2 decimales
- **ISBN**: Opcional, único si se proporciona

### Manejo de Errores

- **Base de Datos**: Captura de errores SQLite
- **Validación**: Excepciones personalizadas con mensajes claros
- **Búsquedas**: Manejo de resultados vacíos

## Optimizaciones de Rendimiento

### Índices de Búsqueda

- **Búsqueda por substring**: Indexación automática de substrings de nombres
- **Búsquedas cruzadas**: Índices separados por autor, categoría, ISBN
- **Conjuntos para unicidad**: Uso de sets para garantizar IDs únicos

### Caching en Memoria

- **Carga inicial**: Todos los productos se cargan al iniciar
- **Actualización sincronizada**: Base de datos y memoria se mantienen sincronizadas

## Extensibilidad del Sistema

### Posibles Mejoras

1. **Usuarios y Autenticación**: Sistema de login y roles
2. **Ventas y Facturación**: Módulo de gestión de ventas
3. **Proveedores**: Gestión de proveedores y pedidos
4. **Reportes Avanzados**: PDFs y gráficos estadísticos
5. **Notificaciones**: Alertas de stock bajo por email

### Nuevas Clases

```python
# Ejemplo de extensión
class Venta:
    def __init__(self, id_venta, id_producto, cantidad, fecha):
        # Implementación de gestión de ventas
        pass

class Proveedor:
    def __init__(self, id_proveedor, nombre, contacto):
        # Implementación de gestión de proveedores
        pass
```

## Contribución

Este sistema está diseñado como base para proyectos académicos y puede ser extendido según las necesidades específicas de cada librería o negocio.

## Licencia

Proyecto educativo desarrollado para la asignatura de Programación.

---

**Autor**: Marleyth Alcivar  
**Fecha**: Marzo 2026  
**Versión**: 1.0
