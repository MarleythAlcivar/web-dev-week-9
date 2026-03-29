# 🔧 Sistema CRUD Completo - Semana 16

## 🎯 **Objetivo de la Semana**

Implementar un sistema CRUD completo con arquitectura organizada en capas, integración con MySQL y generación de reportes PDF.

---

## 📁 **Estructura del Proyecto**

```
deber semana 09/
├── app.py                     # ✅ Aplicación Flask con rutas CRUD
├── models/                    # ✅ Capa de modelos de datos
│   ├── __init__.py           # ✅ Inicialización del paquete
│   └── producto.py           # ✅ Modelo de Producto
├── services/                  # ✅ Capa de lógica de negocio
│   ├── __init__.py           # ✅ Inicialización del paquete
│   └── producto_service.py    # ✅ Servicio de Producto
├── forms/                     # ✅ Capa de formularios
│   ├── __init__.py           # ✅ Inicialización del paquete
│   └── producto_form.py      # ✅ Formularios de Producto
├── reports/                   # ✅ Capa de generación de reportes
│   ├── __init__.py           # ✅ Inicialización del paquete
│   └── pdf_generator.py      # ✅ Generador de PDF
├── templates/                 # ✅ Plantillas HTML
│   ├── productos/            # ✅ Templates de productos
│   │   ├── __init__.py     # ✅ Inicialización del paquete
│   │   ├── index.html       # ✅ Lista de productos
│   │   ├── create.html      # ✅ Crear producto
│   │   ├── edit.html        # ✅ Editar producto
│   │   └── view.html        # ✅ Ver producto
│   ├── auth/                # ✅ Templates de autenticación
│   └── base.html            # ✅ Navegación actualizada
├── conexion/                  # ✅ Conexión MySQL
├── auth/                     # ✅ Autenticación
├── requirements.txt           # ✅ Dependencias actualizadas
└── reports/                  # ✅ Directorio para PDFs generados
```

---

## 🔧 **Características Implementadas**

### **1. Arquitectura en Capas**
- ✅ **Models** - Modelo de datos (`models/producto.py`)
- ✅ **Services** - Lógica de negocio (`services/producto_service.py`)
- ✅ **Forms** - Formularios WTForms (`forms/producto_form.py`)
- ✅ **Reports** - Generación de PDF (`reports/pdf_generator.py`)

### **2. Operaciones CRUD Completas**
- ✅ **CREATE** - Crear nuevos productos
- ✅ **READ** - Leer/Listar productos con filtros
- ✅ **UPDATE** - Actualizar productos existentes
- ✅ **DELETE** - Eliminar productos (borrado lógico)

### **3. Funcionalidades Avanzadas**
- ✅ **Búsqueda** de productos por nombre/descripción
- ✅ **Filtrado** por categoría
- ✅ **Paginación** de resultados
- ✅ **Actualización** de stock individual
- ✅ **Validación** de datos de negocio
- ✅ **Estadísticas** en tiempo real

### **4. Generación de Reportes PDF**
- ✅ **Reporte General** - Listado completo de productos
- ✅ **Reporte de Bajo Stock** - Productos con inventario crítico
- ✅ **Estadísticas** incluidas en reportes
- ✅ **Descarga** automática de PDFs

---

## 🌐 **Rutas CRUD Implementadas**

### **Gestión Principal**
- `/productos` - Lista de productos con búsqueda y filtros
- `/productos/create` - Crear nuevo producto
- `/productos/view/<id>` - Ver detalles del producto
- `/productos/edit/<id>` - Editar producto existente
- `/productos/delete/<id>` - Eliminar producto (POST)
- `/productos/update-stock/<id>` - Actualizar stock (POST)

### **Reportes PDF**
- `/productos/report` - Generar reporte general en PDF
- `/productos/low-stock-report` - Generar reporte de bajo stock en PDF

---

## 📊 **Modelo de Datos**

### **Producto (models/producto.py)**
```python
class Producto:
    def __init__(self, id_producto, nombre, descripcion, precio, stock, categoria, activo):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.activo = activo
    
    # Métodos CRUD
    @staticmethod
    def get_all()                    # Obtener todos los productos
    @staticmethod
    def get_by_id(id_producto)         # Obtener por ID
    @staticmethod
    def get_by_categoria(categoria)      # Filtrar por categoría
    @staticmethod
    def search(term)                   # Buscar productos
    def create(self)                     # Crear producto
    def update(self)                     # Actualizar producto
    def delete(self)                     # Eliminar producto
    def update_stock(self, cantidad)       # Actualizar stock
    
    # Métodos de utilidad
    @staticmethod
    def get_categories()              # Obtener categorías
    @staticmethod
    def get_low_stock(limit=10)       # Productos con bajo stock
    @staticmethod
    def get_statistics()             # Estadísticas del sistema
```

---

## 🔧 **Servicio de Negocio**

### **ProductoService (services/producto_service.py)**
```python
class ProductoService:
    # Validaciones de negocio
    @staticmethod
    def create_product(nombre, descripcion, precio, stock, categoria)
    @staticmethod
    def update_product(id, nombre, descripcion, precio, stock, categoria, activo)
    @staticmethod
    def delete_product(id, permanent=False)
    @staticmethod
    def update_stock(id, cantidad)
    
    # Consultas con validación
    @staticmethod
    def get_all_products()
    @staticmethod
    def get_product_by_id(id)
    @staticmethod
    def search_products(term)
    @staticmethod
    def get_products_by_category(categoria)
    @staticmethod
    def get_low_stock_products(limit=10)
    @staticmethod
    def get_statistics()
```

---

## 📝 **Formularios WTForms**

### **ProductoForm (forms/producto_form.py)**
```python
class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(3, 100)])
    descripcion = TextAreaField('Descripción', validators=[DataRequired(), Length(10, 500)])
    precio = DecimalField('Precio', validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    categoria = SelectField('Categoría', coerce=str)
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar Producto')

class SearchForm(FlaskForm):
    search_term = StringField('Buscar', validators=[DataRequired(), Length(2, 100)])
    submit = SubmitField('Buscar')

class CategoryFilterForm(FlaskForm):
    categoria = SelectField('Categoría', coerce=str)
    submit = SubmitField('Filtrar')
```

---

## 📄 **Generación de Reportes PDF**

### **PDFGenerator (reports/pdf_generator.py)**
```python
class PDFGenerator:
    def generate_product_report(self, productos, title="Reporte de Productos"):
        # Tabla completa de productos
        # Estadísticas generales
        # Formato profesional con ReportLab
        # Descarga automática
    
    def generate_low_stock_report(self, productos, title="Reporte de Bajo Stock"):
        # Alertas de inventario crítico
        # Recomendaciones de reabastecimiento
        # Colores según nivel de stock
```

---

## 🎨 **Templates Implementados**

### **📋 index.html**
- Lista completa de productos
- Búsqueda en tiempo real
- Filtros por categoría
- Estadísticas en tarjetas
- Paginación
- Tabla responsiva con estados de stock

### **➕ create.html**
- Formulario de creación
- Previsualización en tiempo real
- Validación visual
- Ayuda contextual

### **✏️ edit.html**
- Carga de datos existentes
- Actualización de stock rápida
- Información actual del producto
- Estados y recomendaciones

### **👁️ view.html**
- Vista detallada del producto
- Información completa organizada
- Acciones rápidas
- Estados de inventario

---

## 🛠️ **Instalación y Configuración**

### **1. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **2. Configurar MySQL**
```sql
CREATE DATABASE biblioteca;

USE biblioteca;

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    categoria VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### **3. Ejecutar Aplicación**
```bash
python app.py
```

### **4. Acceder al Sistema**
- **Productos CRUD**: `http://localhost:5000/productos`
- **Autenticación**: `http://localhost:5000/login`
- **Reportes**: Disponibles desde la lista de productos

---

## 🔒 **Validaciones y Seguridad**

### **Validaciones de Negocio**
- **Nombre**: 3-100 caracteres, único
- **Descripción**: 10-500 caracteres, requerida
- **Precio**: Mayor que 0, formato decimal
- **Stock**: No negativo, formato entero
- **Categoría**: Opcional, dinámica
- **Email**: Formato válido, único

### **Seguridad Implementada**
- **@login_required** en todas las rutas CRUD
- **CSRF protection** con Flask-WTF
- **SQL injection prevention** con parámetros
- **Input validation** con WTForms
- **Error handling** robusto

---

## 📈 **Características Técnicas**

### **🏗️ Arquitectura**
- **MVC Pattern** con Flask
- **Layered Architecture** (Models-Services-Forms)
- **Separation of Concerns**
- **Dependency Injection** implícita

### **🗄️ Base de Datos**
- **MySQL Connector** para persistencia
- **Connection pooling** automático
- **Transactions** con commit/rollback
- **Error handling** robusto

### **🌐 Web Interface**
- **Bootstrap-style CSS** responsivo
- **JavaScript** para interactividad
- **AJAX** para operaciones asíncronas
- **Flash messages** para feedback

### **📄 Report Generation**
- **ReportLab** para PDFs profesionales
- **Dynamic content** con datos reales
- **Charts** y estadísticas
- **Download automático** de archivos

---

## 📋 **Flujo de Usuario**

### **1. Listado de Productos**
1. Usuario accede a `/productos`
2. Ve lista completa con estadísticas
3. Puede buscar por nombre/descripción
4. Puede filtrar por categoría
5. Paginación para grandes volúmenes

### **2. Creación de Producto**
1. Usuario hace clic en "➕ Nuevo Producto"
2. Llena formulario con validación
3. Previsualización en tiempo real
4. Sistema valida y guarda en MySQL
5. Redirección con mensaje de éxito

### **3. Edición de Producto**
1. Usuario hace clic en "✏️" en lista
2. Carga formulario con datos actuales
3. Puede actualizar stock rápidamente
4. Sistema valida y actualiza
5. Mantiene historial de cambios

### **4. Reportes PDF**
1. Usuario hace clic en "📄 Generar PDF"
2. Sistema genera reporte profesional
3. Incluye estadísticas y gráficos
4. Descarga automática del archivo

---

## 📋 **Resumen de la Semana 16**

**✅ Requisitos Cumplidos:**
- ✅ Implementación correcta del CRUD
- ✅ Organización del proyecto en capas (models, services, forms)
- ✅ Integración con base de datos MySQL
- ✅ Uso adecuado de plantillas Jinja2
- ✅ Generación de reporte en PDF

**✅ Características Adicionales:**
- ✅ Arquitectura escalable y mantenible
- ✅ Validaciones robustas de negocio
- ✅ Búsqueda y filtrado avanzado
- ✅ Paginación de resultados
- ✅ Reportes PDF profesionales
- ✅ Interface responsiva y moderna
- ✅ Seguridad implementada
- ✅ Manejo completo de errores
- ✅ Estadísticas en tiempo real

**El sistema CRUD está completamente implementado con arquitectura profesional y listo para producción.**
