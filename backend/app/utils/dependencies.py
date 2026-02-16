"""
Dependencias de FastAPI.
Funciones que se inyectan en los endpoints para:
- Obtener el usuario actual
- Verificar permisos
- Validar tokens
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.user import User, UserRole
from app.utils.security import decode_token

# Esquema de seguridad Bearer
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Obtiene el usuario actual desde el token JWT.
    
    Esta función se usa como dependencia en endpoints protegidos.
    Valida el token y devuelve el usuario autenticado.
    
    Args:
        credentials: Credenciales del header Authorization
        db: Sesión de base de datos
    
    Returns:
        Usuario autenticado
    
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    
    Uso:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user": current_user.username}
    """
    # Extraer token del header "Authorization: Bearer <token>"
    token = credentials.credentials
    
    # Decodificar token
    payload = decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar que sea un access token
    if payload.get("token_type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obtener ID del usuario desde el token
    user_id: Optional[int] = payload.get("user_id")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Buscar usuario en la base de datos
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar que el usuario esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verifica que el usuario actual esté activo.
    
    Esta es una capa adicional de validación.
    
    Args:
        current_user: Usuario actual
    
    Returns:
        Usuario activo
    
    Raises:
        HTTPException: Si el usuario no está activo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user


async def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verifica que el usuario actual sea administrador.
    
    Uso en endpoints que solo admins pueden acceder:
        @app.delete("/users/{id}")
        def delete_user(
            user_id: int,
            admin: User = Depends(require_admin)
        ):
            # Solo admins pueden llegar aquí
            pass
    
    Args:
        current_user: Usuario actual
    
    Returns:
        Usuario administrador
    
    Raises:
        HTTPException: Si el usuario no es admin
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return current_user


async def require_role(required_role: UserRole):
    """
    Factory para crear dependencias de roles específicos.
    
    Esta es una función más flexible que permite requerir cualquier rol.
    
    Uso:
        @app.get("/admin-only")
        def admin_only(user: User = Depends(require_role(UserRole.ADMIN))):
            pass
    
    Args:
        required_role: Rol requerido
    
    Returns:
        Función de dependencia
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol: {required_role.value}"
            )
        return current_user
    
    return role_checker


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Obtiene el usuario si hay token, pero no es obligatorio.
    
    Útil para endpoints que pueden funcionar con o sin autenticación,
    pero cambian su comportamiento si el usuario está autenticado.
    
    Args:
        credentials: Credenciales opcionales
        db: Sesión de base de datos
    
    Returns:
        Usuario si está autenticado, None si no
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        payload = decode_token(token)
        
        if payload is None or payload.get("token_type") != "access":
            return None
        
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user if user and user.is_active else None
    
    except Exception:
        return None
