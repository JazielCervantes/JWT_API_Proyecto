"""
Repositorio base genérico con operaciones CRUD.
Proporciona una clase base para todos los repositorios específicos.
Reduce duplicación de código y facilita testing.
"""
from typing import TypeVar, Generic, Type, List, Optional, Callable, Any
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from abc import ABC, abstractmethod

# TypeVar para hacer la clase genérica sobre el modelo
T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    """
    Repositorio base genérico para operaciones CRUD.
    
    Proporciona:
    - Create (crear registros)
    - Read (obtener registros por ID, con filtros, lista paginada)
    - Update (actualizar registros existentes)
    - Delete (eliminar registros)
    
    Uso:
    ```python
    class UserRepository(BaseRepository[User]):
        pass
    
    repo = UserRepository(db, User)
    user = repo.get_by_id(1)
    users = repo.get_all(skip=0, limit=10)
    ```
    """
    
    def __init__(self, db: Session, model: Type[T]):
        """
        Inicializa el repositorio.
        
        Args:
            db: Sesión de SQLAlchemy
            model: Clase del modelo SQLAlchemy
        """
        self.db = db
        self.model = model
    
    # ========== CREATE ==========
    def create(self, obj_in: dict | Any) -> T:
        """
        Crea un nuevo registro en la base de datos.
        
        Args:
            obj_in: Diccionario o modelo Pydantic con datos
        
        Returns:
            Objeto creado con ID asignado
        """
        # Convertir Pydantic a diccionario si es necesario
        if hasattr(obj_in, 'model_dump'):
            obj_in = obj_in.model_dump(exclude_unset=True)
        elif hasattr(obj_in, 'dict'):  # Para versiones antiguas de Pydantic
            obj_in = obj_in.dict(exclude_unset=True)
        
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        
        return db_obj
    
    # ========== READ ==========
    def get_by_id(self, obj_id: int) -> Optional[T]:
        """
        Obtiene un registro por su ID.
        
        Args:
            obj_id: ID del registro
        
        Returns:
            Objeto encontrado o None
        """
        return self.db.query(self.model).filter(self.model.id == obj_id).first()
    
    def get_by_field(self, field_name: str, field_value: Any) -> Optional[T]:
        """
        Obtiene un registro por un campo específico.
        
        Args:
            field_name: Nombre del campo (atributo del modelo)
            field_value: Valor a buscar
        
        Returns:
            Primer objeto encontrado o None
        
        Raises:
            AttributeError: Si el campo no existe en el modelo
        """
        if not hasattr(self.model, field_name):
            raise AttributeError(f"El modelo {self.model.__name__} no tiene el campo '{field_name}'")
        
        return self.db.query(self.model).filter(
            getattr(self.model, field_name) == field_value
        ).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict] = None,
        order_by: Optional[str] = None
    ) -> tuple[List[T], int]:
        """
        Obtiene lista de registros con paginación y filtros.
        
        Args:
            skip: Número de registros a saltar (offset)
            limit: Número máximo de registros (límite por página)
            filters: Diccionario {campo: valor} para filtrar
            order_by: Campo por el cual ordenar (ej: 'created_at', '-updated_at' para DESC)
        
        Returns:
            Tupla (lista de registros, total de registros)
        """
        query = self.db.query(self.model)
        
        # Aplicar filtros
        if filters:
            for field_name, field_value in filters.items():
                if not hasattr(self.model, field_name):
                    continue  # Ignorar filtros inválidos
                
                if isinstance(field_value, (list, tuple)):
                    # Filtro IN
                    query = query.filter(getattr(self.model, field_name).in_(field_value))
                else:
                    # Filtro igualdad
                    query = query.filter(getattr(self.model, field_name) == field_value)
        
        # Contar total antes de paginar
        total = query.count()
        
        # Aplicar ordenamiento
        if order_by:
            if order_by.startswith("-"):
                # Descendente
                field_name = order_by[1:]
                if hasattr(self.model, field_name):
                    query = query.order_by(getattr(self.model, field_name).desc())
            else:
                # Ascendente
                if hasattr(self.model, order_by):
                    query = query.order_by(getattr(self.model, order_by))
        
        # Aplicar paginación
        records = query.offset(skip).limit(limit).all()
        
        return records, total
    
    def filter_by(
        self,
        filters: dict,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[T], int]:
        """
        Filtra registros por múltiples criterios.
        Alias más legible para get_all().
        
        Args:
            filters: Diccionario {campo: valor}
            skip: Offset de paginación
            limit: Límite de paginación
        
        Returns:
            Tupla (registros filtrados, total)
        """
        return self.get_all(skip=skip, limit=limit, filters=filters)
    
    # ========== UPDATE ==========
    def update(self, obj_id: int, obj_in: dict | Any) -> Optional[T]:
        """
        Actualiza un registro existente.
        
        Args:
            obj_id: ID del registro a actualizar
            obj_in: Diccionario o Pydantic con datos a actualizar
        
        Returns:
            Objeto actualizado o None si no existe
        """
        db_obj = self.get_by_id(obj_id)
        
        if not db_obj:
            return None
        
        # Convertir Pydantic a diccionario si es necesario
        if hasattr(obj_in, 'model_dump'):
            obj_data = obj_in.model_dump(exclude_unset=True)
        elif hasattr(obj_in, 'dict'):
            obj_data = obj_in.dict(exclude_unset=True)
        else:
            obj_data = obj_in
        
        # Actualizar cada campo
        for field, value in obj_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        
        return db_obj
    
    def bulk_update(self, updates: List[tuple[int, dict]]) -> List[T]:
        """
        Actualiza múltiples registros en batch.
        
        Args:
            updates: Lista de tuplas (id, datos_actualización)
        
        Returns:
            Lista de objetos actualizados
        """
        updated_objects = []
        
        for obj_id, obj_data in updates:
            updated_obj = self.update(obj_id, obj_data)
            if updated_obj:
                updated_objects.append(updated_obj)
        
        return updated_objects
    
    # ========== DELETE ==========
    def delete(self, obj_id: int) -> bool:
        """
        Elimina un registro por ID (hard delete).
        
        Args:
            obj_id: ID del registro a eliminar
        
        Returns:
            True si fue eliminado, False si no existe
        """
        db_obj = self.get_by_id(obj_id)
        
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        
        return True
    
    def soft_delete(self, obj_id: int, inactivate_field: str = "is_active") -> Optional[T]:
        """
        Marca un registro como inactivo (soft delete).
        Requiere que el modelo tenga un campo is_active o similar.
        
        Args:
            obj_id: ID del registro
            inactivate_field: Nombre del campo booleano para marcar como inactivo
        
        Returns:
            Objeto actualizado o None
        """
        db_obj = self.get_by_id(obj_id)
        
        if not db_obj or not hasattr(db_obj, inactivate_field):
            return None
        
        setattr(db_obj, inactivate_field, False)
        self.db.commit()
        self.db.refresh(db_obj)
        
        return db_obj
    
    # ========== UTILITY METHODS ==========
    def exists_by_id(self, obj_id: int) -> bool:
        """
        Verifica si un registro existe por ID.
        
        Args:
            obj_id: ID a verificar
        
        Returns:
            True si existe, False en caso contrario
        """
        return self.db.query(self.model).filter(self.model.id == obj_id).first() is not None
    
    def exists_by_field(self, field_name: str, field_value: Any) -> bool:
        """
        Verifica si un registro existe con un valor de campo específico.
        
        Args:
            field_name: Nombre del campo
            field_value: Valor a buscar
        
        Returns:
            True si existe, False en caso contrario
        """
        if not hasattr(self.model, field_name):
            return False
        
        return self.db.query(self.model).filter(
            getattr(self.model, field_name) == field_value
        ).first() is not None
    
    def count(self, filters: Optional[dict] = None) -> int:
        """
        Cuenta registros con filtros opcionales.
        
        Args:
            filters: Diccionario {campo: valor} para filtrar
        
        Returns:
            Número total de registros que coinciden
        """
        query = self.db.query(self.model)
        
        if filters:
            for field_name, field_value in filters.items():
                if hasattr(self.model, field_name):
                    query = query.filter(getattr(self.model, field_name) == field_value)
        
        return query.count()
    
    def delete_all_filtered(self, filters: dict) -> int:
        """
        Elimina todos los registros que coinciden con filtros.
        ⚠️ USO CAUTELOSO - Esta operación es irreversible.
        
        Args:
            filters: Diccionario {campo: valor}
        
        Returns:
            Número de registros eliminados
        """
        query = self.db.query(self.model)
        
        for field_name, field_value in filters.items():
            if hasattr(self.model, field_name):
                query = query.filter(getattr(self.model, field_name) == field_value)
        
        count = query.delete()
        self.db.commit()
        
        return count
