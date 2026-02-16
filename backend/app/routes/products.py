"""
Rutas de productos.
Endpoints para gestión de productos con CRUD completo, paginación y filtros.
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse
)
from app.schemas.auth import MessageResponse
from app.models.user import User
from app.models.product import Product
from app.utils.dependencies import get_current_user, require_admin, get_optional_user

router = APIRouter(prefix="/products", tags=["Productos"])


@router.get(
    "",
    response_model=ProductListResponse,
    summary="Listar productos",
    description="""
    Lista productos con paginación y filtros avanzados.
    
    - Endpoint público (no requiere autenticación)
    - Soporta búsqueda, filtros y ordenamiento
    """
)
def list_products(
    skip: int = Query(0, ge=0, description="Offset para paginación"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad de resultados"),
    search: Optional[str] = Query(None, description="Buscar en nombre y descripción"),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    brand: Optional[str] = Query(None, description="Filtrar por marca"),
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    in_stock: Optional[bool] = Query(None, description="Solo productos en stock"),
    is_active: bool = Query(True, description="Solo productos activos"),
    sort_by: Optional[str] = Query("created_at", description="Campo para ordenar (name, price, created_at)"),
    order: Optional[str] = Query("desc", description="Orden (asc/desc)"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """
    Lista productos con filtros avanzados.
    
    **Ejemplos de uso:**
    
    Búsqueda simple:
    ```
    GET /api/products?search=laptop
    ```
    
    Filtros múltiples:
    ```
    GET /api/products?category=Electrónica&min_price=500&max_price=2000
    ```
    
    Con paginación y ordenamiento:
    ```
    GET /api/products?skip=0&limit=20&sort_by=price&order=asc
    ```
    """
    query = db.query(Product)
    
    # Filtro de estado activo
    if is_active is not None:
        query = query.filter(Product.is_active == is_active)
    
    # Búsqueda por texto
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Product.name.like(search_filter)) |
            (Product.description.like(search_filter))
        )
    
    # Filtro por categoría
    if category:
        query = query.filter(Product.category == category)
    
    # Filtro por marca
    if brand:
        query = query.filter(Product.brand == brand)
    
    # Filtro por rango de precio
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    # Filtro por stock
    if in_stock:
        query = query.filter(Product.stock > 0)
    
    # Ordenamiento
    if sort_by == "name":
        query = query.order_by(Product.name.desc() if order == "desc" else Product.name.asc())
    elif sort_by == "price":
        query = query.order_by(Product.price.desc() if order == "desc" else Product.price.asc())
    else:  # default: created_at
        query = query.order_by(Product.created_at.desc() if order == "desc" else Product.created_at.asc())
    
    # Contar total
    total = query.count()
    
    # Aplicar paginación
    products = query.offset(skip).limit(limit).all()
    
    return ProductListResponse(
        products=products,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Obtener producto por ID",
    description="Obtiene la información detallada de un producto"
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un producto por su ID.
    
    **Ejemplo:**
    ```
    GET /api/products/1
    ```
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    
    return product


# ============= ENDPOINTS SOLO PARA ADMINISTRADORES =============


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear producto (Admin)",
    description="Crea un nuevo producto. Requiere rol de administrador."
)
def create_product(
    product: ProductCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo producto.
    
    Requiere rol de administrador.
    
    **Ejemplo de request:**
    ```json
    {
        "name": "Laptop Dell XPS 15",
        "description": "Laptop de alto rendimiento",
        "price": 1299.99,
        "stock": 10,
        "category": "Electrónica",
        "brand": "Dell",
        "sku": "DELL-XPS15-001"
    }
    ```
    """
    # Verificar si el SKU ya existe
    if product.sku:
        existing = db.query(Product).filter(Product.sku == product.sku).first()
        if existing:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El SKU ya existe"
            )
    
    # Crear producto
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Actualizar producto (Admin)",
    description="Actualiza un producto existente. Requiere rol de administrador."
)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Actualiza un producto.
    
    Requiere rol de administrador.
    
    **Ejemplo de request:**
    ```json
    {
        "price": 1199.99,
        "stock": 15
    }
    ```
    """
    # Buscar producto
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    
    # Actualizar campos
    update_data = product_update.model_dump(exclude_unset=True)
    
    # Verificar SKU único si se actualiza
    if "sku" in update_data and update_data["sku"] != product.sku:
        existing = db.query(Product).filter(Product.sku == update_data["sku"]).first()
        if existing:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El SKU ya existe"
            )
    
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    return product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar producto (Admin)",
    description="Elimina un producto (soft delete). Requiere rol de administrador."
)
def delete_product(
    product_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Elimina (desactiva) un producto.
    
    Requiere rol de administrador.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    
    # Soft delete
    product.is_active = False
    db.commit()
    
    return None


@router.get(
    "/categories/list",
    response_model=list[str],
    summary="Listar categorías",
    description="Obtiene todas las categorías de productos disponibles"
)
def list_categories(
    db: Session = Depends(get_db)
):
    """
    Lista todas las categorías únicas de productos.
    
    **Ejemplo de response:**
    ```json
    ["Electrónica", "Ropa", "Hogar", "Deportes"]
    ```
    """
    categories = db.query(Product.category).distinct().filter(
        Product.category.isnot(None),
        Product.is_active == True
    ).all()
    
    return [cat[0] for cat in categories if cat[0]]


@router.get(
    "/brands/list",
    response_model=list[str],
    summary="Listar marcas",
    description="Obtiene todas las marcas de productos disponibles"
)
def list_brands(
    db: Session = Depends(get_db)
):
    """
    Lista todas las marcas únicas de productos.
    """
    brands = db.query(Product.brand).distinct().filter(
        Product.brand.isnot(None),
        Product.is_active == True
    ).all()
    
    return [brand[0] for brand in brands if brand[0]]
