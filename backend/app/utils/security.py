"""
Utilidades de seguridad.
Manejo de contraseñas hasheadas y tokens JWT.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings
from app.models.user import UserRole

# Contexto para hashear contraseñas con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash.
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña hasheada
    
    Returns:
        True si coinciden, False si no
    
    Ejemplo:
        >>> verify_password("mi_password", "$2b$12$...")
        True
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro de una contraseña.
    
    Args:
        password: Contraseña en texto plano
    
    Returns:
        Hash de la contraseña
    
    Ejemplo:
        >>> get_password_hash("mi_password")
        '$2b$12$...'
    
    Nota:
        Bcrypt genera un salt único por cada hash,
        por eso la misma contraseña produce hashes diferentes.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT de acceso.
    
    Args:
        data: Datos a incluir en el token (user_id, username, role)
        expires_delta: Tiempo de expiración personalizado
    
    Returns:
        Token JWT codificado
    
    Ejemplo:
        >>> token = create_access_token({"user_id": 1, "username": "user"})
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    """
    to_encode = data.copy()
    
    # Establecer tiempo de expiración
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Agregar datos adicionales al token
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),  # Issued at (fecha de emisión)
        "token_type": "access"
    })
    
    # Codificar el token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Crea un token JWT de refresco.
    
    Los refresh tokens tienen mayor duración y se usan
    para obtener nuevos access tokens sin requerir login.
    
    Args:
        data: Datos a incluir en el token
    
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    
    # Refresh token con mayor duración
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "token_type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Decodifica y valida un token JWT.
    
    Args:
        token: Token JWT a decodificar
    
    Returns:
        Datos del token si es válido, None si no
    
    Ejemplo:
        >>> payload = decode_token(token)
        >>> print(payload['user_id'])
        1
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def create_tokens_for_user(user_id: int, username: str, role: UserRole) -> tuple[str, str]:
    """
    Crea ambos tokens (access y refresh) para un usuario.
    
    Args:
        user_id: ID del usuario
        username: Username del usuario
        role: Rol del usuario
    
    Returns:
        Tupla (access_token, refresh_token)
    
    Ejemplo:
        >>> access, refresh = create_tokens_for_user(1, "usuario", UserRole.USER)
    """
    token_data = {
        "user_id": user_id,
        "username": username,
        "role": role.value
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return access_token, refresh_token
