"""
Módulo de repositorios.

Proporciona acceso a datos mediante el patrón Repository:
- BaseRepository: CRUD genérico para todos los modelos
- UserRepository: Queries específicas para usuarios
- ProductRepository: Queries específicas para productos

Ventajas del patrón Repository:
1. ✅ Elimina duplicación de queries
2. ✅ Centraliza lógica de acceso a datos
3. ✅ Facilita testing (se pueden mockerear)
4. ✅ Cambiar BD sin afectar servicios
5. ✅ Queries legibles y reutilizables
"""
from app.repositories.base import BaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "ProductRepository",
]
