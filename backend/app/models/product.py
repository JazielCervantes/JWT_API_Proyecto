"""
Modelo de Producto para la base de datos.
Define la estructura de la tabla 'products' en MySQL.
Este es un ejemplo de un recurso que se puede gestionar con CRUD.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    """
    Modelo de Producto.
    
    Ejemplo de un recurso para demostrar:
    - CRUD completo
    - Paginación
    - Filtros
    - Búsqueda
    """
    __tablename__ = "products"
    
    # ID auto-incremental
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Información del producto
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    
    # Categoría y marca
    category = Column(String(100), nullable=True, index=True)
    brand = Column(String(100), nullable=True)
    
    # SKU (Stock Keeping Unit) - código único del producto
    sku = Column(String(50), unique=True, index=True, nullable=True)
    
    # Estado
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Auditoría
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        """Representación del objeto para debugging"""
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "brand": self.brand,
            "sku": self.sku,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
