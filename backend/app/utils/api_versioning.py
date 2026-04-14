"""
Utilidad para versionamiento de API.

Proporciona helpers para crear y manejar múltiples versiones de API
con mínimo esfuerzo.

Ejemplo uso:
```python
from app.utils.api_versioning import get_versioned_router

# Crear routers para múltiples versiones
routers_v1 = get_versioned_router("v1", auth, users, products)

for version, routers in routers_v1.items():
    for router in routers:
        app.include_router(router, prefix=f"/api/v1")
```
"""
from typing import List, Dict, Any, Tuple
from fastapi import APIRouter


class APIVersionManager:
    """
    Gestor centralizado de versiones de API.
    
    Permite:
    - Registrar múltiples versiones
    - Obtener rutas versionadas
    - Listar versiones soportadas
    """
    
    def __init__(self):
        self.versions: Dict[str, Dict[str, Any]] = {}
    
    def register_version(
        self,
        version: str,
        description: str = "",
        deprecated: bool = False
    ) -> None:
        """
        Registra una nueva versión de API.
        
        Args:
            version: Identificador de versión (ej: "v1", "v2")
            description: Descripción de cambios en esta versión
            deprecated: Marcar versión como deprecada
        """
        self.versions[version] = {
            "description": description,
            "deprecated": deprecated,
            "routers": []
        }
    
    def add_router(self, version: str, router: APIRouter) -> None:
        """
        Agrrega un router a una versión específica.
        
        Args:
            version: Versión de API
            router: Router de FastAPI a agregar
        """
        if version not in self.versions:
            self.register_version(version)
        
        self.versions[version]["routers"].append(router)
    
    def get_version_info(self, version: str) -> Dict[str, Any]:
        """Obtiene información de una versión específica."""
        return self.versions.get(version, {})
    
    def get_supported_versions(self) -> List[str]:
        """Retorna lista de versiones soportadas."""
        return list(self.versions.keys())
    
    def get_active_versions(self) -> List[str]:
        """Retorna solo versiones activas (no deprecadas)."""
        return [
            version for version, info in self.versions.items()
            if not info.get("deprecated", False)
        ]
    
    def get_deprecated_versions(self) -> List[str]:
        """Retorna solo versiones deprecadas."""
        return [
            version for version, info in self.versions.items()
            if info.get("deprecated", False)
        ]
    
    def get_routers_for_version(self, version: str) -> List[APIRouter]:
        """Obtiene todos los routers para una versión."""
        return self.versions.get(version, {}).get("routers", [])


# Instancia global del gestor
version_manager = APIVersionManager()


def create_versioned_endpoints(
    version: str,
    base_path: str,
    routers: List[APIRouter],
    app: Any
) -> None:
    """
    Helper para incluir múltiples routers versionados en la app.
    
    Uso:
    ```python
    from app.routes import auth, users, products
    from app.utils.api_versioning import create_versioned_endpoints
    
    create_versioned_endpoints(
        version="v1",
        base_path="/api/v1",
        routers=[auth.router, users.router, products.router],
        app=app
    )
    ```
    
    Args:
        version: Número de versión
        base_path: Path base (ej: "/api/v1")
        routers: Lista de routers a incluir
        app: Aplicación FastAPI
    """
    version_manager.register_version(version)
    
    for router in routers:
        app.include_router(router, prefix=base_path)
        version_manager.add_router(version, router)


@app.get("/api/versions", tags=["API Versions"])
def get_api_versions():
    """
    Endpoint para obtener información sobre versiones de API.
    
    Útil para clientes que necesitan saber qué versiones están disponibles.
    """
    versions_info = {}
    
    for version in version_manager.get_supported_versions():
        info = version_manager.get_version_info(version)
        versions_info[version] = {
            "description": info.get("description", ""),
            "deprecated": info.get("deprecated", False),
            "path": f"/api/{version}",
            "router_count": len(info.get("routers", []))
        }
    
    return {
        "active_versions": version_manager.get_active_versions(),
        "deprecated_versions": version_manager.get_deprecated_versions(),
        "versions": versions_info
    }
