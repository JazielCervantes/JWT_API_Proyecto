"""
Rutas de autenticación.
Endpoints para registro, login, refresh y logout.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    MessageResponse
)
from app.services.auth_service import AuthService
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="""
    Crea un nuevo usuario en el sistema.
    
    - Email y username deben ser únicos
    - La contraseña debe tener mínimo 6 caracteres
    - Se asigna automáticamente el rol 'user'
    """
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint de registro de usuarios.
    
    **Ejemplo de request:**
    ```json
    {
        "email": "usuario@ejemplo.com",
        "username": "usuario123",
        "password": "contraseña123",
        "full_name": "Juan Pérez"
    }
    ```
    """
    return AuthService.register_user(db, user_data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    description="""
    Autentica al usuario y retorna tokens JWT.
    
    - Puedes usar email o username para iniciar sesión
    - Retorna access token (corta duración) y refresh token (larga duración)
    - El access token debe incluirse en el header Authorization: Bearer <token>
    """
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint de login.
    
    **Ejemplo de request:**
    ```json
    {
        "username": "usuario123",
        "password": "contraseña123"
    }
    ```
    
    **Ejemplo de response:**
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    }
    ```
    """
    return AuthService.login(db, credentials.username, credentials.password)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refrescar access token",
    description="""
    Obtiene un nuevo access token usando el refresh token.
    
    - Usa esto cuando el access token expire
    - El refresh token tiene mayor duración
    - Retorna nuevos access y refresh tokens
    """
)
def refresh_token(
    token_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint para refrescar tokens.
    
    **Ejemplo de request:**
    ```json
    {
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
    """
    return AuthService.refresh_access_token(db, token_request.refresh_token)


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Cerrar sesión",
    description="""
    Cierra la sesión del usuario actual.
    
    - Invalida el refresh token en el servidor
    - Requiere estar autenticado
    """
)
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint de logout.
    
    Requiere token de autenticación en el header:
    ```
    Authorization: Bearer <access_token>
    ```
    """
    AuthService.logout(db, current_user)
    return MessageResponse(message="Sesión cerrada exitosamente")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener usuario actual",
    description="""
    Retorna la información del usuario autenticado.
    
    - Requiere token válido
    - Útil para verificar autenticación
    """
)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint para obtener información del usuario actual.
    
    Requiere token de autenticación en el header:
    ```
    Authorization: Bearer <access_token>
    ```
    """
    return current_user
