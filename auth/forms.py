"""
Formularios de autenticación
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class LoginForm(FlaskForm):
    """Formulario de inicio de sesión"""
    email = StringField('Email', validators=[
        DataRequired(message='El email es requerido'),
        Email(message='Ingrese un email válido')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es requerida'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegisterForm(FlaskForm):
    """Formulario de registro de usuarios"""
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='El email es requerido'),
        Email(message='Ingrese un email válido'),
        Length(max=100, message='El email no puede tener más de 100 caracteres')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es requerida'),
        Length(min=6, max=128, message='La contraseña debe tener entre 6 y 128 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Debe confirmar la contraseña'),
        EqualTo('password', message='Las contraseñas no coinciden')
    ])
    submit = SubmitField('Registrarse')

class ProfileForm(FlaskForm):
    """Formulario de perfil de usuario"""
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='El email es requerido'),
        Email(message='Ingrese un email válido'),
        Length(max=100, message='El email no puede tener más de 100 caracteres')
    ])
    submit = SubmitField('Actualizar Perfil')

class ChangePasswordForm(FlaskForm):
    """Formulario de cambio de contraseña"""
    current_password = PasswordField('Contraseña Actual', validators=[
        DataRequired(message='La contraseña actual es requerida')
    ])
    new_password = PasswordField('Nueva Contraseña', validators=[
        DataRequired(message='La nueva contraseña es requerida'),
        Length(min=6, max=128, message='La contraseña debe tener entre 6 y 128 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Nueva Contraseña', validators=[
        DataRequired(message='Debe confirmar la nueva contraseña'),
        EqualTo('new_password', message='Las contraseñas nuevas no coinciden')
    ])
    submit = SubmitField('Cambiar Contraseña')
