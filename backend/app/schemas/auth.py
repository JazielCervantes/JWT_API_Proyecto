"""
Schemas de Autenticación usando Pydantic.
Define cómo se validan los datos de login y tokens.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.user import UserRole


class LoginRequest(BaseModel):
    """
    Schema para solicitud de login.
    El usuario puede iniciar sesión con username o email.
    """
    username: str = Field(..., description="Username o email del usuario")
    password: str = Field(..., description="Contraseña del usuario")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "usuario123",
                "password": "contraseña123"
            }
        }
    )


class TokenResponse(BaseModel):
    """
    Schema de respuesta con tokens.
    Se devuelve después de un login exitoso.
    """
    access_token: str = Field(..., description="Token de acceso (JWT)")
    refresh_token: str = Field(..., description="Token de refresco (JWT)")
    token_type: str = Field(default="bearer", description="Tipo de token")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )


class RefreshTokenRequest(BaseModel):
    """
    Schema para refrescar el token de acceso.
    """
    refresh_token: str = Field(..., description="Token de refresco")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    )


class TokenData(BaseModel):
    """
    Schema de datos contenidos en el token JWT.
    Se usa internamente para validación.
    """
    user_id: int
    username: str
    role: UserRole
    token_type: str  # "access" o "refresh"


class PasswordChange(BaseModel):
    """
    Schema para cambiar la contraseña.
    """
    current_password: str = Field(..., description="Contraseña actual")
    new_password: str = Field(..., min_length=6, description="Nueva contraseña")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "current_password": "contraseña_antigua",
                "new_password": "contraseña_nueva123"
            }
        }
    )


class MessageResponse(BaseModel):
    """
    Schema genérico para respuestas con mensaje.
    """
    message: str = Field(..., description="Mensaje de respuesta")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Operación exitosa"
            }
        }
    )
