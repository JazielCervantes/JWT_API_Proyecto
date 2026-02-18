"""
Aplicación principal FastAPI.
Punto de entrada de la API REST.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.config import settings
from app.database import get_db, init_db

from app.models.user import User, UserRole
from app.utils.security import get_password_hash


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación.
    Se ejecuta al inicio y al final de la aplicación.
    """
    # Código de inicio
    print("🚀 Iniciando aplicación...")
    
    # Inicializar base de datos
    print("📦 Inicializando base de datos...")
    init_db()
    
    # Crear usuario admin si no existe
    print("👤 Verificando usuario administrador...")
    create_admin_if_not_exists()
    
    print("✅ Aplicación iniciada correctamente")
    print(f"📖 Documentación disponible en: http://localhost:8000/docs")
    
    yield
    
    # Código de limpieza (al cerrar)
    print("👋 Cerrando aplicación...")


# Crear instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    API REST profesional con autenticación JWT y sistema de roles.
    
    ## Características
    
    * 🔐 **Autenticación JWT** con access y refresh tokens
    * 👥 **Sistema de Roles** (Admin/User)
    * 🔒 **Hash de contraseñas** con bcrypt
    * 🛡️ **Protección de endpoints** por roles
    * 📄 **Paginación** de resultados
    * 🔍 **Filtros** avanzados
    * ⚠️ **Manejo de errores** profesional
    * 📚 **Documentación automática** con Swagger
    
    ## Autenticación
    
    1. Registra un usuario en `/api/auth/register`
    2. Inicia sesión en `/api/auth/login` para obtener tokens
    3. Usa el access_token en el header: `Authorization: Bearer <token>`
    4. Cuando el access_token expire, usa `/api/auth/refresh` con el refresh_token
    
    ## Roles
    
    - **user**: Usuario normal con acceso limitado
    - **admin**: Administrador con acceso total
    
    ## Credenciales de Admin
    
    - Username: `admin`
    - Password: `admin123`
    - Email: `admin@ejemplo.com`
    
    ⚠️ **IMPORTANTE**: Cambiar estas credenciales en producción
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

origins = [
    "https://jwt-api-frontend.vercel.app",  # tu frontend en producción
]

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)


# Manejador de errores de validación
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Maneja errores de validación de Pydantic.
    Retorna un formato más amigable de errores.
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Error de validación",
            "errors": errors
        }
    )


# Manejador de errores generales
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Maneja errores no capturados.
    En producción, no mostrar detalles del error.
    """
    if settings.DEBUG:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Error interno del servidor",
                "error": str(exc),
                "type": type(exc).__name__
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Error interno del servidor"
            }
        )

from app.routes import auth, users, products

# Incluir rutas
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(products.router, prefix="/api")


# Endpoint raíz
@app.get("/", tags=["Root"])
def root():
    """
    Endpoint raíz de la API.
    Retorna información básica de la API.
    """
    return {
        "message": "¡Bienvenido a la API REST Profesional!",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "online"
    }


# Endpoint de salud
@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint de salud para verificar que la API está funcionando.
    Útil para monitoreo y load balancers.
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


def create_admin_if_not_exists():
    """
    Crea el usuario administrador por defecto si no existe.
    Se ejecuta al iniciar la aplicación.
    """
    db: Session = next(get_db())
    
    try:
        # Verificar si ya existe un admin
        admin_exists = db.query(User).filter(User.role == UserRole.ADMIN).first()
        
        if not admin_exists:
            print("📝 Creando usuario administrador por defecto...")
            
            # Crear admin
            admin = User(
                email=settings.ADMIN_EMAIL,
                username=settings.ADMIN_USERNAME,
                full_name=settings.ADMIN_FULL_NAME,
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                role=UserRole.ADMIN,
                is_active=True
            )
            
            db.add(admin)
            db.commit()
            
            print(f"✅ Usuario admin creado: {settings.ADMIN_USERNAME}")
            print(f"   Email: {settings.ADMIN_EMAIL}")
            print(f"   Password: {settings.ADMIN_PASSWORD}")
            print("   ⚠️  CAMBIAR CONTRASEÑA EN PRODUCCIÓN")
        else:
            print("✅ Usuario administrador ya existe")
    
    except Exception as e:
        print(f"❌ Error al crear admin: {e}")
        db.rollback()
    
    finally:
        db.close()


# Para ejecutar con: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
