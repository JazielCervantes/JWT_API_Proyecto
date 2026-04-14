"""
Schemas de Usuario usando Pydantic.
Define cómo se validan y serializan los datos de usuarios.
"""
import re
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
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
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        """Username solo puede tener letras, números y guiones bajos."""
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username solo puede contener letras, números y guiones bajos (_)")
        return v


class UserCreate(UserBase):
    """
    Schema para crear un usuario.
    Se usa en el endpoint de registro.
    Contraseña FUERTE (8+, UPPER+lower+digit+special).
    """
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Contraseña fuerte (mín 8 caracteres, debe incluir mayúscula, minúscula, número, carácter especial)"
    )
    
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        """
        Valida que la contraseña sea fuerte:
        - Mínimo 8 caracteres
        - Al menos 1 mayúscula
        - Al menos 1 minúscula
        - Al menos 1 número
        - Al menos 1 carácter especial (@$!%*?&)
        """
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Contraseña débil. Requiere: mayúscula, minúscula, número, carácter especial (@$!%*?&)"
            )
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "usuario@ejemplo.com",
                "username": "usuario123",
                "full_name": "Juan Pérez",
                "password": "SecurePass123!"
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
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    is_active: Optional[bool] = None
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        """Username solo puede tener letras, números y guiones bajos."""
        if v is not None and not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username solo puede contener letras, números y guiones bajos (_)")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        """Valida contraseña si se proporciona."""
        if v is not None:
            pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
            if not re.match(pattern, v):
                raise ValueError(
                    "Contraseña débil. Requiere: mayúscula, minúscula, número, carácter especial (@$!%*?&)"
                )
        return v
    
    
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
