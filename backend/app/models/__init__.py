"""
Paquete de modelos de la base de datos.
Aquí se importan todos los modelos para facilitar su uso.
"""
from app.models.user import User
from app.models.product import Product

__all__ = ["User", "Product"]
