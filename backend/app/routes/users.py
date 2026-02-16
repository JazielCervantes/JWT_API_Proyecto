"""
Rutas de usuarios.
Endpoints para gestión de usuarios (CRUD).
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.user import (
    UserResponse,
    UserUpdate,
    UserUpdateRole,
    UserListResponse
)
from app.schemas.auth import PasswordChange, MessageResponse
from app.services.user_service import UserService
from app.utils.dependencies import get_current_user, require_admin
from app.models.user import User, UserRole

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener mi perfil",
    description="Retorna la información del usuario autenticado actual"
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene el perfil del usuario actual.
    
    Requiere autenticación.
    """
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Actualizar mi perfil",
    description="Permite al usuario actualizar su propia información"
)
def update_my_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza el perfil del usuario actual.
    
    **Campos actualizables:**
    - email
    - username
    - full_name
    - password
    
    **Ejemplo de request:**
    ```json
    {
        "full_name": "Nuevo Nombre",
        "email": "nuevo@email.com"
    }
    ```
    """
    return UserService.update_user(db, current_user.id, user_update, current_user)


@router.post(
    "/me/change-password",
    response_model=MessageResponse,
    summary="Cambiar mi contraseña",
    description="Permite al usuario cambiar su contraseña actual"
)
def change_my_password(
    password_change: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cambia la contraseña del usuario actual.
    
    **Ejemplo de request:**
    ```json
    {
        "current_password": "contraseña_antigua",
        "new_password": "contraseña_nueva123"
    }
    ```
    """
    UserService.change_password(
        db,
        current_user,
        password_change.current_password,
        password_change.new_password
    )
    return MessageResponse(message="Contraseña actualizada exitosamente")


# ============= ENDPOINTS SOLO PARA ADMINISTRADORES =============


@router.get(
    "",
    response_model=UserListResponse,
    summary="Listar usuarios (Admin)",
    description="""
    Lista todos los usuarios con paginación y filtros.
    
    **Requiere rol de administrador**
    """
)
def list_users(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros"),
    role: Optional[UserRole] = Query(None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    search: Optional[str] = Query(None, description="Buscar por username, email o nombre"),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Lista usuarios con paginación y filtros.
    
    **Parámetros de consulta:**
    - skip: Offset para paginación
    - limit: Cantidad de resultados (máx 100)
    - role: Filtrar por rol (user/admin)
    - is_active: Filtrar por estado
    - search: Búsqueda por texto
    
    **Ejemplo de uso:**
    ```
    GET /api/users?skip=0&limit=10&role=user&search=juan
    ```
    """
    users, total = UserService.get_users(
        db,
        skip=skip,
        limit=limit,
        role=role,
        is_active=is_active,
        search=search
    )
    
    return UserListResponse(
        users=users,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID (Admin)",
    description="Obtiene la información de un usuario específico por su ID"
)
def get_user(
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Obtiene un usuario por su ID.
    
    Requiere rol de administrador.
    """
    return UserService.get_user_by_id(db, user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario (Admin)",
    description="Permite a un administrador actualizar cualquier usuario"
)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Actualiza un usuario específico.
    
    Requiere rol de administrador.
    
    **Ejemplo de request:**
    ```json
    {
        "is_active": false,
        "full_name": "Usuario Actualizado"
    }
    ```
    """
    return UserService.update_user(db, user_id, user_update, admin)


@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
    summary="Cambiar rol de usuario (Admin)",
    description="Permite a un administrador cambiar el rol de un usuario"
)
def update_user_role(
    user_id: int,
    role_update: UserUpdateRole,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Cambia el rol de un usuario.
    
    Requiere rol de administrador.
    
    **Ejemplo de request:**
    ```json
    {
        "role": "admin"
    }
    ```
    """
    return UserService.update_user_role(db, user_id, role_update)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario (Admin)",
    description="""
    Elimina un usuario (soft delete).
    
    - No elimina físicamente, solo marca como inactivo
    - El administrador no puede eliminarse a sí mismo
    """
)
def delete_user(
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Elimina (desactiva) un usuario.
    
    Requiere rol de administrador.
    """
    UserService.delete_user(db, user_id, admin)
    return None
