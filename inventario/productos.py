"""
Modelo SQLAlchemy para Producto
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .bd import Base

class Producto(Base):
    """
    Modelo SQLAlchemy para la tabla de productos
    """
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    autor = Column(String(255), nullable=True, index=True)
    categoria = Column(String(100), nullable=True, index=True)
    isbn = Column(String(20), nullable=True, unique=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', cantidad={self.cantidad}, precio={self.precio})>"
    
    def to_dict(self):
        """
        Convertir el objeto a diccionario
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio': self.precio,
            'autor': self.autor,
            'categoria': self.categoria,
            'isbn': self.isbn,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
