"""
Modelo de Usuario para la base de datos.
Define la estructura de la tabla 'users' en MySQL.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from datetime import datetime
import enum
from app.database import Base


class UserRole(str, enum.Enum):
    """
    Enumeración de roles de usuario.
    Define los roles permitidos en el sistema.
    """
    USER = "user"      # Usuario normal
    ADMIN = "admin"    # Administrador con todos los permisos


class User(Base):
    """
    Modelo de Usuario.
    
    Representa un usuario en el sistema con:
    - Credenciales de acceso (email, username, password)
    - Información personal (full_name)
    - Control de acceso (role, is_active)
    - Auditoría (created_at, updated_at)
    """
    __tablename__ = "users"
    
    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Credenciales - unique=True evita duplicados
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  # Contraseña hasheada
    
    # Información personal
    full_name = Column(String(100), nullable=False)
    
    # Control de acceso
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Auditoría - se llenan automáticamente
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Token de refresh (se guarda para poder invalidarlo)
    refresh_token = Column(String(500), nullable=True)
    
    def __repr__(self):
        """Representación del objeto para debugging"""
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
    
    def to_dict(self):
        """Convierte el modelo a diccionario (útil para respuestas JSON)"""
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "role": self.role.value,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
