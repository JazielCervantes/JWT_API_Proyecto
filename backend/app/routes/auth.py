"""
Rutas de autenticación.
Endpoints para registro, login, refresh y logout.

⭐ FASE 3 REFACTORING:
- AuthService inyecta UserRepository
- Rutas usan AuthService como instancia
- Dependencias manejan la inyección automáticamente
- Código más testeable y mantenible
"""
from fastapi import APIRouter, Depends, Request, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    MessageResponse
)
from app.services.auth_service import AuthService
from app.utils.dependencies import get_current_user, get_user_repository
from app.core import logger
from app.middleware import limiter
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
    - Contraseña FUERTE: 8+ caracteres, mayúscula, minúscula, número, carácter especial
    - Se asigna automáticamente el rol 'user'
    """
)
@limiter.limit("3/hour")  # Max 3 registros por hora por IP
def register(
    request: Request,
    user_data: UserCreate,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """
    Endpoint de registro de usuarios con rate limiting (3/hora).
    
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
    # Crear instancia del servicio con repositorio inyectado
    auth_service = AuthService(user_repo)
    return auth_service.register_user(user_data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    description="""
    Autentica al usuario y retorna tokens JWT.
    
    - Rate limit: 5 intentos/minuto por IP
    - Refresh token se guarda en HTTP-Only cookie (seguro contra XSS)
    - Access token se retorna en JSON body
    - El access token debe incluirse en el header: Authorization: Bearer <token>
    """
)
@limiter.limit("5/minute")  # Max 5 intentos por minuto por IP (brute force protection)
def login(
    request: Request,
    credentials: LoginRequest,
    user_repo: UserRepository = Depends(get_user_repository),
    response: Response = None
):
    """
    Endpoint de login con rate limiting (5/minuto) y HTTP-Only cookies.
    """
    # Crear instancia del servicio con repositorio inyectado
    auth_service = AuthService(user_repo)
    
    # Autenticar y obtener tokens
    tokens = auth_service.login(credentials.username, credentials.password)
    
    # ✅ Guardar refresh token en HTTP-Only cookie (protección contra XSS)
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        max_age=7*24*60*60,  # 7 días
        httponly=True,       # JavaScript NO puede acceder
        secure=True,         # HTTPS only
        samesite="strict"    # CSRF protection
    )
    
    # ✅ Retornar solo access_token en JSON (refresh está en cookie)
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,  # Frontend puede ignorar esto
        token_type="bearer"
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refrescar access token",
    description="""
    Obtiene un nuevo access token usando el refresh token.
    
    - Rate limit: 10 intentos/minuto
    - El refresh token se obtiene de la cookie HTTP-Only
    - Retorna nuevo access token + refresh token
    """
)
@limiter.limit("10/minute")  # Rate limit para refresh
def refresh_token(
    request: Request,
    token_request: RefreshTokenRequest,
    user_repo: UserRepository = Depends(get_user_repository),
    response: Response = None
):
    """
    Endpoint para refrescar tokens con rate limiting.
    Obtiene el refresh token de la cookie HTTP-Only.
    """
    # Crear instancia del servicio
    auth_service = AuthService(user_repo)
    
    # Intentar obtener refresh token de:
    # 1. Cookie HTTP-Only (preferido)
    # 2. Body JSON (fallback para compatibilidad)
    refresh_token_value = request.cookies.get("refresh_token") or token_request.refresh_token
    
    # Refrescar
    tokens = auth_service.refresh_access_token(refresh_token_value)
    
    # ✅ Actualizar cookie con nuevo refresh token
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        max_age=7*24*60*60,
        httponly=True,
        secure=True,
        samesite="strict"
    )
    
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type="bearer"
    )


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
    user_repo: UserRepository = Depends(get_user_repository)
):
    """
    Endpoint de logout.
    
    Requiere token de autenticación en el header:
    ```
    Authorization: Bearer <access_token>
    ```
    """
    # Crear instancia del servicio
    auth_service = AuthService(user_repo)
    auth_service.logout(current_user)
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
