"""
Schemas de Producto usando Pydantic.
Define cómo se validan y serializan los datos de productos.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    """
    Schema base de producto.
    Campos comunes a varios schemas.
    """
    name: str = Field(..., min_length=1, max_length=200, description="Nombre del producto")
    description: Optional[str] = Field(None, description="Descripción del producto")
    price: float = Field(..., gt=0, description="Precio del producto (debe ser mayor a 0)")
    stock: int = Field(default=0, ge=0, description="Cantidad en stock")
    category: Optional[str] = Field(None, max_length=100, description="Categoría del producto")
    brand: Optional[str] = Field(None, max_length=100, description="Marca del producto")
    sku: Optional[str] = Field(None, max_length=50, description="SKU (código único)")


class ProductCreate(ProductBase):
    """
    Schema para crear un producto.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop Dell XPS 15",
                "description": "Laptop de alto rendimiento",
                "price": 1299.99,
                "stock": 10,
                "category": "Electrónica",
                "brand": "Dell",
                "sku": "DELL-XPS15-001"
            }
        }
    )


class ProductUpdate(BaseModel):
    """
    Schema para actualizar un producto.
    Todos los campos son opcionales.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    sku: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "price": 1199.99,
                "stock": 15
            }
        }
    )


class ProductResponse(ProductBase):
    """
    Schema de respuesta de producto.
    """
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Laptop Dell XPS 15",
                "description": "Laptop de alto rendimiento",
                "price": 1299.99,
                "stock": 10,
                "category": "Electrónica",
                "brand": "Dell",
                "sku": "DELL-XPS15-001",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }
    )


class ProductListResponse(BaseModel):
    """
    Schema para lista de productos con paginación.
    """
    products: list[ProductResponse]
    total: int
    skip: int
    limit: int
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "products": [],
                "total": 100,
                "skip": 0,
                "limit": 10
            }
        }
    )


class ProductFilters(BaseModel):
    """
    Schema para filtros de búsqueda de productos.
    """
    search: Optional[str] = Field(None, description="Búsqueda por nombre o descripción")
    category: Optional[str] = Field(None, description="Filtrar por categoría")
    brand: Optional[str] = Field(None, description="Filtrar por marca")
    min_price: Optional[float] = Field(None, ge=0, description="Precio mínimo")
    max_price: Optional[float] = Field(None, ge=0, description="Precio máximo")
    in_stock: Optional[bool] = Field(None, description="Solo productos en stock")
    is_active: Optional[bool] = Field(True, description="Solo productos activos")
