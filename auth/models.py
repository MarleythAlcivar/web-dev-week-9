"""
Modelos de autenticación para Flask-Login
"""

from conexion.models import Usuario
from flask_login import UserMixin

class User(UserMixin):
    """Modelo de usuario para Flask-Login"""
    
    def __init__(self, usuario_db):
        self.id = usuario_db.id_usuario
        self.id_usuario = usuario_db.id_usuario
        self.nombre = usuario_db.nombre
        self.mail = usuario_db.mail
        self.password = usuario_db.password
        self.fecha_registro = usuario_db.fecha_registro
        self.activo = usuario_db.activo
    
    @staticmethod
    def get_by_id(user_id):
        """Obtener usuario por ID para Flask-Login"""
        usuario_db = Usuario.get_by_id(user_id)
        if usuario_db:
            return User(usuario_db)
        return None
    
    @staticmethod
    def get_by_mail(email):
        """Obtener usuario por email para autenticación"""
        usuario_db = Usuario.get_by_mail(email)
        if usuario_db:
            return User(usuario_db)
        return None
    
    def verify_password(self, password):
        """Verificar contraseña"""
        return Usuario.hash_password(password) == self.password
    
    def is_active(self):
        """Verificar si el usuario está activo"""
        return self.activo
    
    def get_id(self):
        """Obtener ID del usuario para Flask-Login"""
        return str(self.id)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'mail': self.mail,
            'fecha_registro': self.fecha_registro,
            'activo': self.activo
        }
