"""
Configuración de base de datos con SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite:///inventario_sqlalchemy.db"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=False)

# Crear la clase base para los modelos
Base = declarative_base()

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Función para obtener una sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Inicializar la base de datos creando todas las tablas
    """
    Base.metadata.create_all(bind=engine)
