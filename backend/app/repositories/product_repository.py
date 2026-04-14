"""
Repositorio específico de productos.
Extiende BaseRepository con queries especializadas para Product.
"""
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Repositorio para operaciones específicas de productos.
    
    Extiende BaseRepository con:
    - Búsqueda por nombre, SKU, categoría
    - Búsqueda con filtros de precio, stock, estado
    - Búsqueda con texto libre
    - Gestión de inventario
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el repositorio de productos.
        
        Args:
            db: Sesión de SQLAlchemy
        """
        super().__init__(db, Product)
    
    # ========== BÚSQUEDAS ESPECÍFICAS ==========
    
    def get_by_sku(self, sku: str) -> Optional[Product]:
        """
        Obtiene un producto por su SKU (Stock Keeping Unit).
        
        Args:
            sku: SKU único del producto
        
        Returns:
            Producto encontrado o None
        """
        return self.get_by_field("sku", sku)
    
    def get_by_name(self, name: str) -> Optional[Product]:
        """
        Obtiene el primer producto con nombre exacto.
        
        Args:
            name: Nombre del producto
        
        Returns:
            Producto encontrado o None
        """
        return self.db.query(Product).filter(Product.name == name).first()
    
    def search_products(
        self,
        search_query: str,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[Product], int]:
        """
        Busca productos por texto libre en nombre y descripción.
        
        Args:
            search_query: Texto a buscar
            skip: Offset de paginación
            limit: Límite de paginación
            category: Filtrar por categoría
            brand: Filtrar por marca
            is_active: Filtrar por estado activo
        
        Returns:
            Tupla (productos encontrados, total)
        """
        search_filter = f"%{search_query}%"
        query = self.db.query(Product).filter(
            (Product.name.ilike(search_filter)) |
            (Product.description.ilike(search_filter))
        )
        
        # Aplicar filtros adicionales
        if category:
            query = query.filter(Product.category == category)
        
        if brand:
            query = query.filter(Product.brand == brand)
        
        if is_active is not None:
            query = query.filter(Product.is_active == is_active)
        
        # Contar total
        total = query.count()
        
        # Aplicar paginación
        products = query.offset(skip).limit(limit).all()
        
        return products, total
    
    def get_by_category(
        self,
        category: str,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> Tuple[List[Product], int]:
        """
        Obtiene productos filtrados por categoría.
        
        Args:
            category: Categoría a buscar
            skip: Offset
            limit: Límite
            is_active: Filtrar por estado
        
        Returns:
            Tupla (productos, total)
        """
        filters = {"category": category}
        if is_active is not None:
            filters["is_active"] = is_active
        
        return self.filter_by(filters, skip=skip, limit=limit)
    
    def get_by_brand(
        self,
        brand: str,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> Tuple[List[Product], int]:
        """
        Obtiene productos filtrados por marca.
        
        Args:
            brand: Marca a buscar
            skip: Offset
            limit: Límite
            is_active: Filtrar por estado
        
        Returns:
            Tupla (productos, total)
        """
        filters = {"brand": brand}
        if is_active is not None:
            filters["is_active"] = is_active
        
        return self.filter_by(filters, skip=skip, limit=limit)
    
    def get_active_products(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Product], int]:
        """
        Obtiene solo productos activos.
        
        Args:
            skip: Offset
            limit: Límite
        
        Returns:
            Tupla (productos activos, total)
        """
        return self.filter_by({"is_active": True}, skip=skip, limit=limit)
    
    # ========== GESTIÓN DE INVENTARIO ==========
    
    def get_low_stock_products(
        self,
        threshold: int = 10,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Product], int]:
        """
        Obtiene productos con stock bajo (menos del umbral).
        
        Args:
            threshold: Umbral considerado bajo
            skip: Offset
            limit: Límite
        
        Returns:
            Tupla (productos con stock bajo, total)
        """
        query = self.db.query(Product).filter(
            (Product.stock < threshold) & (Product.is_active == True)
        )
        
        total = query.count()
        products = query.offset(skip).limit(limit).all()
        
        return products, total
    
    def get_out_of_stock_products(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Product], int]:
        """
        Obtiene productos sin stock.
        
        Args:
            skip: Offset
            limit: Límite
        
        Returns:
            Tupla (productos sin stock, total)
        """
        query = self.db.query(Product).filter(
            (Product.stock == 0) & (Product.is_active == True)
        )
        
        total = query.count()
        products = query.offset(skip).limit(limit).all()
        
        return products, total
    
    def increase_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        """
        Aumenta el stock de un producto.
        
        Args:
            product_id: ID del producto
            quantity: Cantidad a aumentar (debe ser positivo)
        
        Returns:
            Producto actualizado o None
        """
        if quantity < 0:
            raise ValueError("La cantidad debe ser positiva")
        
        product = self.get_by_id(product_id)
        if not product:
            return None
        
        product.stock += quantity
        self.db.commit()
        self.db.refresh(product)
        
        return product
    
    def decrease_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        """
        Disminuye el stock de un producto (para ventas).
        
        Args:
            product_id: ID del producto
            quantity: Cantidad a disminuir
        
        Returns:
            Producto actualizado o None
        
        Raises:
            ValueError: Si cantidad es negativa o hay stock insuficiente
        """
        if quantity < 0:
            raise ValueError("La cantidad debe ser positiva")
        
        product = self.get_by_id(product_id)
        if not product:
            return None
        
        if product.stock < quantity:
            raise ValueError(f"Stock insuficiente. Disponible: {product.stock}, Solicitado: {quantity}")
        
        product.stock -= quantity
        self.db.commit()
        self.db.refresh(product)
        
        return product
    
    def set_stock(self, product_id: int, new_quantity: int) -> Optional[Product]:
        """
        Establece el stock de un producto a un valor específico.
        
        Args:
            product_id: ID del producto
            new_quantity: Nuevo valor de stock
        
        Returns:
            Producto actualizado o None
        
        Raises:
            ValueError: Si new_quantity es negativo
        """
        if new_quantity < 0:
            raise ValueError("El stock no puede ser negativo")
        
        product = self.get_by_id(product_id)
        if not product:
            return None
        
        product.stock = new_quantity
        self.db.commit()
        self.db.refresh(product)
        
        return product
    
    # ========== BÚSQUEDAS POR RANGO DE PRECIOS ==========
    
    def get_by_price_range(
        self,
        min_price: float = 0,
        max_price: Optional[float] = None,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> Tuple[List[Product], int]:
        """
        Obtiene productos dentro de un rango de precios.
        
        Args:
            min_price: Precio mínimo
            max_price: Precio máximo (None = sin límite)
            skip: Offset
            limit: Límite
            is_active: Filtrar por estado
        
        Returns:
            Tupla (productos en rango, total)
        """
        query = self.db.query(Product).filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        if is_active is not None:
            query = query.filter(Product.is_active == is_active)
        
        total = query.count()
        products = query.offset(skip).limit(limit).all()
        
        return products, total
    
    def get_most_expensive(
        self,
        limit: int = 10,
        is_active: Optional[bool] = None
    ) -> List[Product]:
        """
        Obtiene los productos más caros.
        
        Args:
            limit: Número de productos a retornar
            is_active: Filtrar por estado
        
        Returns:
            Lista de productos ordenados por precio (descendente)
        """
        query = self.db.query(Product).order_by(Product.price.desc())
        
        if is_active is not None:
            query = query.filter(Product.is_active == is_active)
        
        return query.limit(limit).all()
    
    def get_cheapest(
        self,
        limit: int = 10,
        is_active: Optional[bool] = None
    ) -> List[Product]:
        """
        Obtiene los productos más baratos.
        
        Args:
            limit: Número de productos a retornar
            is_active: Filtrar por estado
        
        Returns:
            Lista de productos ordenados por precio (ascendente)
        """
        query = self.db.query(Product).order_by(Product.price.asc())
        
        if is_active is not None:
            query = query.filter(Product.is_active == is_active)
        
        return query.limit(limit).all()
    
    # ========== ESTADÍSTICAS DE INVENTARIO ==========
    
    def get_inventory_stats(self) -> dict:
        """
        Obtiene estadísticas del inventario.
        
        Returns:
            Diccionario con:
            - total_products: Total de productos
            - active_products: Productos activos
            - out_of_stock: Productos sin stock
            - total_stock_value: Valor total del inventario
            - low_stock_count: Productos con stock bajo
        """
        from sqlalchemy import func
        
        total = self.db.query(Product).count()
        active = self.db.query(Product).filter(Product.is_active == True).count()
        out_of_stock = self.db.query(Product).filter(Product.stock == 0).count()
        
        # Valor total del inventario
        total_value = self.db.query(
            func.sum(Product.price * Product.stock)
        ).filter(Product.is_active == True).scalar() or 0
        
        # Productos con stock bajo (< 10)
        low_stock = self.db.query(Product).filter(
            (Product.stock < 10) & (Product.is_active == True)
        ).count()
        
        return {
            "total_products": total,
            "active_products": active,
            "out_of_stock": out_of_stock,
            "total_stock_value": float(total_value),
            "low_stock_count": low_stock
        }
