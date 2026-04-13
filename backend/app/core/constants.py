"""
Constantes globales - Mensajes de error y valores por defecto.
"""

# Mensajes de error (para consistencia)
ERROR_MESSAGES = {
    # Auth
    "USER_NOT_FOUND": "Usuario no encontrado",
    "INVALID_CREDENTIALS": "Credenciales inválidas",
    "USER_ALREADY_EXISTS": "Usuario ya existe",
    "INVALID_EMAIL": "Email no es válido",
    "INVALID_TOKEN": "Token inválido u expirado",
    "TOKEN_EXPIRED": "Token expirado",
    "REFRESH_TOKEN_REVOKED": "Token de refresco ha sido revocado",
    
    # Permissions
    "PERMISSION_DENIED": "Permiso denegado",
    "ADMIN_REQUIRED": "Se requieren permisos de administrador",
    
    # Validation
    "VALIDATION_ERROR": "Error de validación",
    "WEAK_PASSWORD": "Contraseña débil. Requiere: mayúscula, minúscula, número, carácter especial (@$!%*?&)",
    "PASSWORD_TOO_SHORT": "Contraseña muy corta (mínimo 8 caracteres)",
    "INVALID_USERNAME": "Username válido solo con letras, números, y _",
    
    # Resources
    "RESOURCE_NOT_FOUND": "Recurso no encontrado",
    "PRODUCT_NOT_FOUND": "Producto no encontrado",
    "USER_INACTIVE": "Usuario inactivo",
    
    # Database
    "DATABASE_ERROR": "Error de base de datos",
    
    # Rate limiting
    "RATE_LIMIT_EXCEEDED": "Demasiadas solicitudes. Intenta más tarde.",
}

# Validaciones
PASSWORD_MIN_LENGTH = 8
PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"  # UPPER+lower+digit+special
USERNAME_PATTERN = r"^[a-zA-Z0-9_]{3,50}$"  # Alphanumeric + underscore, 3-50 chars

# Paginación
DEFAULT_SKIP = 0
DEFAULT_LIMIT = 20
MAX_LIMIT = 100

# JWT
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 min (más corto, más seguro)
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Logs
LOG_LEVEL = "INFO"
