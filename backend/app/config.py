"""
Configuración de la aplicación.
Maneja todas las variables de entorno y configuraciones globales.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic.
    Lee automáticamente las variables de entorno del archivo .env
    """
    
    # Información de la aplicación
    APP_NAME: str = "API REST Profesional"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Base de datos
    DATABASE_URL: str
    
    # JWT (JSON Web Tokens)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS - Lista de orígenes permitidos para hacer peticiones
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:4321"
    
    # Admin por defecto
    ADMIN_EMAIL: str = "admin@ejemplo.com"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    ADMIN_FULL_NAME: str = "Administrador del Sistema"
    
    @property
    def origins_list(self) -> List[str]:
        """Convierte la cadena de orígenes en una lista"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        # Indica que debe leer del archivo .env
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
# Se puede importar en cualquier parte: from app.config import settings
settings = Settings()
