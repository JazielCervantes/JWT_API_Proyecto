"""
Servicio de usuarios.
Lógica de negocio para gestión de usuarios.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.user import User, UserRole
from app.schemas.user import UserUpdate, UserUpdateRole
from app.utils.security import get_password_hash, verify_password


class UserService:
    """
    Servicio de usuarios.
    Maneja operaciones CRUD y gestión de usuarios.
    """
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """
        Obtiene un usuario por su ID.
        
        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
        
        Returns:
            Usuario encontrado
        
        Raises:
            HTTPException: Si el usuario no existe
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        return user
    
    @staticmethod
    def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None
    ) -> tuple[List[User], int]:
        """
        Obtiene lista de usuarios con paginación y filtros.
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            role: Filtrar por rol
            is_active: Filtrar por estado activo
            search: Buscar por username, email o nombre
        
        Returns:
            Tupla (lista de usuarios, total de registros)
        """
        query = db.query(User)
        
        # Aplicar filtros
        if role is not None:
            query = query.filter(User.role == role)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (User.username.like(search_filter)) |
                (User.email.like(search_filter)) |
                (User.full_name.like(search_filter))
            )
        
        # Contar total antes de paginar
        total = query.count()
        
        # Aplicar paginación
        users = query.offset(skip).limit(limit).all()
        
        return users, total
    
    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        user_update: UserUpdate,
        current_user: User
    ) -> User:
        """
        Actualiza un usuario.
        
        Args:
            db: Sesión de base de datos
            user_id: ID del usuario a actualizar
            user_update: Datos a actualizar
            current_user: Usuario que realiza la actualización
        
        Returns:
            Usuario actualizado
        
        Raises:
            HTTPException: Si hay errores de validación o permisos
        """
        # Obtener usuario a actualizar
        user = UserService.get_user_by_id(db, user_id)
        
        # Solo admins pueden actualizar otros usuarios
        if current_user.id != user_id and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para actualizar este usuario"
            )
        
        # Actualizar campos si se proporcionan
        update_data = user_update.model_dump(exclude_unset=True)
        
        # Verificar unicidad de email si se actualiza
        if "email" in update_data and update_data["email"] != user.email:
            existing = db.query(User).filter(User.email == update_data["email"]).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está en uso"
                )
        
        # Verificar unicidad de username si se actualiza
        if "username" in update_data and update_data["username"] != user.username:
            existing = db.query(User).filter(User.username == update_data["username"]).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El username ya está en uso"
                )
        
        # Hashear contraseña si se actualiza
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # Solo admins pueden cambiar is_active
        if "is_active" in update_data and current_user.role != UserRole.ADMIN:
            del update_data["is_active"]
        
        # Aplicar actualizaciones
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def update_user_role(
        db: Session,
        user_id: int,
        role_update: UserUpdateRole
    ) -> User:
        """
        Actualiza el rol de un usuario (solo admin).
        
        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
            role_update: Nuevo rol
        
        Returns:
            Usuario actualizado
        """
        user = UserService.get_user_by_id(db, user_id)
        user.role = role_update.role
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: int, current_user: User) -> None:
        """
        Elimina un usuario (soft delete - lo marca como inactivo).
        
        Args:
            db: Sesión de base de datos
            user_id: ID del usuario a eliminar
            current_user: Usuario que realiza la eliminación
        
        Raises:
            HTTPException: Si no tiene permisos o intenta eliminarse a sí mismo
        """
        # Solo admins pueden eliminar usuarios
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo administradores pueden eliminar usuarios"
            )
        
        # No se puede eliminar a sí mismo
        if current_user.id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes eliminarte a ti mismo"
            )
        
        user = UserService.get_user_by_id(db, user_id)
        
        # Soft delete - marcar como inactivo
        user.is_active = False
        db.commit()
    
    @staticmethod
    def change_password(
        db: Session,
        user: User,
        current_password: str,
        new_password: str
    ) -> None:
        """
        Cambia la contraseña de un usuario.
        
        Args:
            db: Sesión de base de datos
            user: Usuario actual
            current_password: Contraseña actual
            new_password: Nueva contraseña
        
        Raises:
            HTTPException: Si la contraseña actual es incorrecta
        """
        # Verificar contraseña actual
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta"
            )
        
        # Actualizar contraseña
        user.hashed_password = get_password_hash(new_password)
        db.commit()
