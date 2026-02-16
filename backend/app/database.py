"""
Configuración de la base de datos.
Establece la conexión con MySQL usando SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Motor de base de datos
# pool_pre_ping=True verifica la conexión antes de usarla
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG  # Muestra las queries SQL en consola si DEBUG=True
)

# Fábrica de sesiones
# autocommit=False: Los cambios no se guardan automáticamente
# autoflush=False: Los objetos no se sincronizan automáticamente
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos
# Todos los modelos heredarán de esta clase
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos.
    
    Se usa como dependencia en FastAPI:
    - Crea una sesión
    - La proporciona al endpoint
    - La cierra al terminar
    
    Uso:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa la base de datos.
    Crea todas las tablas definidas en los modelos.
    
    IMPORTANTE: Ejecutar esto solo en desarrollo.
    En producción, usar Alembic para migraciones.
    """
    from app.models import user, product  # Importar todos los modelos
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada correctamente")


if __name__ == "__main__":
    # Permite ejecutar: python -m app.database
    # Para crear las tablas
    print("🔧 Creando tablas en la base de datos...")
    init_db()
