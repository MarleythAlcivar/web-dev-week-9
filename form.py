"""
Formularios Flask para la aplicación
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Optional

class ProductoForm(FlaskForm):
    """
    Formulario para agregar/editar productos
    """
    nombre = StringField('Nombre del Producto', 
                        validators=[DataRequired(), Length(min=2, max=255)])
    
    autor = StringField('Autor', 
                       validators=[DataRequired(), Length(min=2, max=255)])
    
    categoria = SelectField('Categoría', 
                           choices=[
                               ('', 'Seleccionar categoría...'),
                               ('Programación', 'Programación'),
                               ('Matemáticas', 'Matemáticas'),
                               ('Física', 'Física'),
                               ('Literatura', 'Literatura'),
                               ('Ciencias', 'Ciencias'),
                               ('Negocios', 'Negocios'),
                               ('Educación', 'Educación')
                           ],
                           validators=[Optional()])
    
    isbn = StringField('ISBN', 
                      validators=[Optional(), Length(max=20)])
    
    cantidad = IntegerField('Cantidad', 
                           validators=[DataRequired(), NumberRange(min=0)])
    
    precio = FloatField('Precio ($)', 
                       validators=[DataRequired(), NumberRange(min=0.0)])
    
    submit = SubmitField('Guardar Producto')
