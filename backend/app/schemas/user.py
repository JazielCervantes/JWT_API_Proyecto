"""
Schemas de Usuario usando Pydantic.
Define cómo se validan y serializan los datos de usuarios.
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """
    Schema base de usuario.
    Campos comunes a varios schemas.
    """
    email: EmailStr = Field(..., description="Email del usuario")
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    full_name: str = Field(..., min_length=2, max_length=100, description="Nombre completo")


class UserCreate(UserBase):
    """
    Schema para crear un usuario.
    Se usa en el endpoint de registro.
    """
    password: str = Field(..., min_length=6, max_length=100, description="Contraseña (mínimo 6 caracteres)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "usuario@ejemplo.com",
                "username": "usuario123",
                "full_name": "Juan Pérez",
                "password": "contraseña123"
            }
        }
    )


class UserUpdate(BaseModel):
    """
    Schema para actualizar un usuario.
    Todos los campos son opcionales.
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    is_active: Optional[bool] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "Juan Pérez Actualizado",
                "email": "nuevo@ejemplo.com"
            }
        }
    )


class UserUpdateRole(BaseModel):
    """
    Schema para actualizar el rol de un usuario (solo admin).
    """
    role: UserRole = Field(..., description="Nuevo rol del usuario")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role": "admin"
            }
        }
    )


class UserResponse(UserBase):
    """
    Schema de respuesta de usuario.
    Lo que se devuelve al cliente (sin contraseña).
    """
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,  # Permite crear desde modelos SQLAlchemy
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "usuario@ejemplo.com",
                "username": "usuario123",
                "full_name": "Juan Pérez",
                "role": "user",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }
    )


class UserListResponse(BaseModel):
    """
    Schema para lista de usuarios con paginación.
    """
    users: list[UserResponse]
    total: int
    skip: int
    limit: int
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "users": [],
                "total": 50,
                "skip": 0,
                "limit": 10
            }
        }
    )
