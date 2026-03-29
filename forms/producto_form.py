"""
Formularios para el sistema CRUD
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ProductoForm(FlaskForm):
    """Formulario para crear/editar productos"""
    
    nombre = StringField('Nombre del Producto', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres')
    ])
    
    descripcion = TextAreaField('Descripción', validators=[
        DataRequired(message='La descripción es requerida'),
        Length(min=10, max=500, message='La descripción debe tener entre 10 y 500 caracteres')
    ])
    
    precio = DecimalField('Precio', validators=[
        DataRequired(message='El precio es requerido'),
        NumberRange(min=0.01, message='El precio debe ser mayor que 0')
    ], places=2)
    
    stock = IntegerField('Stock', validators=[
        DataRequired(message='El stock es requerido'),
        NumberRange(min=0, message='El stock no puede ser negativo')
    ])
    
    categoria = SelectField('Categoría', validators=[
        Optional()
    ], coerce=str)
    
    activo = BooleanField('Activo', default=True)
    
    submit = SubmitField('Guardar Producto')
    
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        # Cargar categorías dinámicamente
        from services.producto_service import ProductoService
        categorias_result = ProductoService.get_categories()
        if categorias_result['success']:
            categorias = categorias_result['data']
            self.categoria.choices = [('', 'Seleccionar categoría...')] + [(cat, cat) for cat in categorias]

class SearchForm(FlaskForm):
    """Formulario para buscar productos"""
    
    search_term = StringField('Buscar', validators=[
        DataRequired(message='Ingrese un término de búsqueda'),
        Length(min=2, max=100, message='El término debe tener entre 2 y 100 caracteres')
    ])
    
    submit = SubmitField('Buscar')

class CategoryFilterForm(FlaskForm):
    """Formulario para filtrar por categoría"""
    
    categoria = SelectField('Categoría', validators=[
        Optional()
    ], coerce=str)
    
    submit = SubmitField('Filtrar')
    
    def __init__(self, *args, **kwargs):
        super(CategoryFilterForm, self).__init__(*args, **kwargs)
        # Cargar categorías dinámicamente
        from services.producto_service import ProductoService
        categorias_result = ProductoService.get_categories()
        if categorias_result['success']:
            categorias = categorias_result['data']
            self.categoria.choices = [('', 'Todas las categorías')] + [(cat, cat) for cat in categorias]

class StockUpdateForm(FlaskForm):
    """Formulario para actualizar stock"""
    
    stock = IntegerField('Nuevo Stock', validators=[
        DataRequired(message='El stock es requerido'),
        NumberRange(min=0, message='El stock no puede ser negativo')
    ])
    
    submit = SubmitField('Actualizar Stock')

class DeleteForm(FlaskForm):
    """Formulario para confirmar eliminación"""
    
    confirm = BooleanField('Confirmar eliminación', validators=[
        DataRequired(message='Debe confirmar la eliminación')
    ])
    
    submit = SubmitField('Eliminar Producto')
