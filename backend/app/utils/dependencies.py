"""
Dependencias de FastAPI.
Funciones que se inyectan en los endpoints para:
- Obtener el usuario actual
- Verificar permisos
- Validar tokens
"""
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.user import User, UserRole
from app.utils.security import decode_token
from app.core import (
    InvalidToken,
    UserNotFound,
    UserInactive,
    PermissionDenied,
    logger,
)

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
        InvalidToken: Si el token es inválido u expirado
        UserNotFound: Si el usuario no existe
        UserInactive: Si el usuario está inactivo
    
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
        logger.warning("Intento de acceso con token inválido o expirado")
        raise InvalidToken(reason="Token expirado o inválido")
    
    # Verificar que sea un access token
    if payload.get("token_type") != "access":
        logger.warning("Intento de acceso con tipo de token incorrecto")
        raise InvalidToken(reason="Tipo de token incorrecto")
    
    # Obtener ID del usuario desde el token
    user_id: Optional[int] = payload.get("user_id")
    
    if user_id is None:
        logger.warning("Token sin user_id")
        raise InvalidToken()
    
    # Buscar usuario en la base de datos
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        logger.warning(f"Usuario no encontrado (ID: {user_id})")
        raise UserNotFound()
    
    # Verificar que el usuario esté activo
    if not user.is_active:
        logger.warning(f"Intento de acceso con usuario inactivo (ID: {user.id})")
        raise UserInactive()
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verifica que el usuario actual esté activo.
    
    Esta es una capa adicional de validación (redundante con get_current_user).
    
    Args:
        current_user: Usuario actual
    
    Returns:
        Usuario activo
    
    Raises:
        UserInactive: Si el usuario no está activo
    """
    if not current_user.is_active:
        logger.warning(f"Usuario inactivo: {current_user.username}")
        raise UserInactive()
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
        PermissionDenied: Si el usuario no es admin
    """
    if current_user.role != UserRole.ADMIN:
        logger.warning(f"Intento de acceso admin sin permiso: {current_user.username}")
        raise PermissionDenied(reason="Se requieren permisos de administrador")
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


# ==============================================================================
# INYECCIÓN DE REPOSITORIOS (FASE 3)
# ==============================================================================

def get_user_repository(db: Session = Depends(get_db)):
    """
    Inyección de dependencia para UserRepository.
    
    Proporciona una instancia del repositorio de usuarios
    con la sesión de BD inyectada.
    
    Uso en rutas:
        from app.repositories import UserRepository
        
        @app.get("/users")
        def list_users(repo: UserRepository = Depends(get_user_repository)):
            users, total = repo.get_all()
            return {"users": users, "total": total}
    
    Args:
        db: Sesión de base de datos
    
    Returns:
        Instancia de UserRepository
    """
    from app.repositories import UserRepository
    return UserRepository(db)


def get_product_repository(db: Session = Depends(get_db)):
    """
    Inyección de dependencia para ProductRepository.
    
    Proporciona una instancia del repositorio de productos
    con la sesión de BD inyectada.
    
    Uso en rutas:
        from app.repositories import ProductRepository
        
        @app.get("/products")
        def list_products(repo: ProductRepository = Depends(get_product_repository)):
            products, total = repo.get_all()
            return {"products": products, "total": total}
    
    Args:
        db: Sesión de base de datos
    
    Returns:
        Instancia de ProductRepository
    """
    from app.repositories import ProductRepository
    return ProductRepository(db)
