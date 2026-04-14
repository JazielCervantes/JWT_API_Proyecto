"""
Repositorio específico de usuarios.
Extiende BaseRepository con queries especializadas para User.
"""
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.repositories.base import BaseRepository
from app.core.exceptions import UserNotFound, UserAlreadyExists
from app.core.logger import logger


class UserRepository(BaseRepository[User]):
    """
    Repositorio para operaciones específicas de usuarios.
    
    Extiende BaseRepository con:
    - Búsqueda por email/username
    - Búsqueda con filtros de role y is_active
    - Búsqueda con texto libre (search)
    - Validación de unicidad
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el repositorio de usuarios.
        
        Args:
            db: Sesión de SQLAlchemy
        """
        super().__init__(db, User)
    
    # ========== BÚSQUEDAS ESPECÍFICAS ==========
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email: Email del usuario (case-sensitive)
        
        Returns:
            Usuario encontrado o None
        """
        return self.get_by_field("email", email)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Obtiene un usuario por su username.
        
        Args:
            username: Username del usuario
        
        Returns:
            Usuario encontrado o None
        """
        return self.get_by_field("username", username)
    
    def get_by_email_or_username(self, identifier: str) -> Optional[User]:
        """
        Obtiene un usuario por email O username.
        Útil para login donde el usuario puede usar cualquiera de los dos.
        
        Args:
            identifier: Email o username
        
        Returns:
            Usuario encontrado o None
        """
        return self.db.query(User).filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()
    
    def search_users(
        self,
        search_query: str,
        skip: int = 0,
        limit: int = 100,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[User], int]:
        """
        Busca usuarios por texto libre con filtros opcionales.
        
        Args:
            search_query: Texto a buscar (en username, email, full_name)
            skip: Offset de paginación
            limit: Límite de paginación
            role: Filtrar por rol (USER, ADMIN)
            is_active: Filtrar por estado
        
        Returns:
            Tupla (usuarios encontrados, total de resultados)
        """
        # Construir búsqueda de texto
        search_filter = f"%{search_query}%"
        query = self.db.query(User).filter(
            (User.username.ilike(search_filter)) |
            (User.email.ilike(search_filter)) |
            (User.full_name.ilike(search_filter))
        )
        
        # Aplicar filtros adicionales
        if role is not None:
            query = query.filter(User.role == role)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        # Contar total antes de paginar
        total = query.count()
        
        # Aplicar paginación
        users = query.offset(skip).limit(limit).all()
        
        return users, total
    
    def get_by_role(
        self,
        role: UserRole,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> Tuple[List[User], int]:
        """
        Obtiene usuarios filtrados por rol.
        
        Args:
            role: Rol a filtrar (USER, ADMIN)
            skip: Offset de paginación
            limit: Límite de paginación
            is_active: Filtrar por estado activo (opcional)
        
        Returns:
            Tupla (usuarios, total)
        """
        filters = {"role": role}
        if is_active is not None:
            filters["is_active"] = is_active
        
        return self.filter_by(filters, skip=skip, limit=limit)
    
    def get_active_users(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[User], int]:
        """
        Obtiene solo usuarios activos.
        
        Args:
            skip: Offset
            limit: Límite
        
        Returns:
            Tupla (usuarios activos, total)
        """
        return self.filter_by({"is_active": True}, skip=skip, limit=limit)
    
    def get_admins(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[User], int]:
        """
        Obtiene lista de administradores.
        
        Args:
            skip: Offset
            limit: Límite
        
        Returns:
            Tupla (admins, total)
        """
        return self.get_by_role(UserRole.ADMIN, skip=skip, limit=limit)
    
    # ========== VALIDACIONES DE UNICIDAD ==========
    
    def email_exists(self, email: str, exclude_user_id: Optional[int] = None) -> bool:
        """
        Verifica si un email ya está registrado.
        
        Args:
            email: Email a validar
            exclude_user_id: ID de usuario a excluir (para actualizaciones)
        
        Returns:
            True si existe, False en caso contrario
        """
        query = self.db.query(User).filter(User.email == email)
        
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        
        return query.first() is not None
    
    def username_exists(self, username: str, exclude_user_id: Optional[int] = None) -> bool:
        """
        Verifica si un username ya está registrado.
        
        Args:
            username: Username a validar
            exclude_user_id: ID de usuario a excluir (para actualizaciones)
        
        Returns:
            True si existe, False en caso contrario
        """
        query = self.db.query(User).filter(User.username == username)
        
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        
        return query.first() is not None
    
    # ========== OPERACIONES BATCH ==========
    
    def get_by_ids(self, user_ids: List[int]) -> List[User]:
        """
        Obtiene múltiples usuarios por sus IDs.
        
        Args:
            user_ids: Lista de IDs
        
        Returns:
            Lista de usuarios encontrados
        """
        return self.db.query(User).filter(User.id.in_(user_ids)).all()
    
    def activate_users(self, user_ids: List[int]) -> int:
        """
        Activa múltiples usuarios.
        
        Args:
            user_ids: Lista de IDs a activar
        
        Returns:
            Número de usuarios activados
        """
        count = self.db.query(User).filter(User.id.in_(user_ids)).update(
            {User.is_active: True}
        )
        self.db.commit()
        return count
    
    def deactivate_users(self, user_ids: List[int]) -> int:
        """
        Desactiva múltiples usuarios.
        
        Args:
            user_ids: Lista de IDs a desactivar
        
        Returns:
            Número de usuarios desactivados
        """
        count = self.db.query(User).filter(User.id.in_(user_ids)).update(
            {User.is_active: False}
        )
        self.db.commit()
        return count
    
    def promote_to_admin(self, user_ids: List[int]) -> int:
        """
        Asciende múltiples usuarios a ADMIN.
        
        Args:
            user_ids: Lista de IDs a ascender
        
        Returns:
            Número de usuarios ascendidos
        """
        count = self.db.query(User).filter(User.id.in_(user_ids)).update(
            {User.role: UserRole.ADMIN}
        )
        self.db.commit()
        return count
    
    def demote_from_admin(self, user_ids: List[int]) -> int:
        """
        Degrada múltiples usuarios de ADMIN a USER.
        
        Args:
            user_ids: Lista de IDs a degradar
        
        Returns:
            Número de usuarios degradados
        """
        count = self.db.query(User).filter(User.id.in_(user_ids)).update(
            {User.role: UserRole.USER}
        )
        self.db.commit()
        return count
    
    # ========== ESTADÍSTICAS ==========
    
    def get_stats(self) -> dict:
        """
        Obtiene estadísticas de usuarios.
        
        Returns:
            Diccionario con:
            - total_users: Total de usuarios
            - active_users: Usuarios activos
            - inactive_users: Usuarios inactivos
            - admin_count: Número de admins
            - user_count: Número de usuarios normales
        """
        total = self.db.query(User).count()
        active = self.db.query(User).filter(User.is_active == True).count()
        inactive = self.db.query(User).filter(User.is_active == False).count()
        admins = self.db.query(User).filter(User.role == UserRole.ADMIN).count()
        regular = self.db.query(User).filter(User.role == UserRole.USER).count()
        
        return {
            "total_users": total,
            "active_users": active,
            "inactive_users": inactive,
            "admin_count": admins,
            "user_count": regular
        }
