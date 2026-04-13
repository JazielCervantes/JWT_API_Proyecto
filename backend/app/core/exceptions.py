"""
Excepciones personalizadas de la aplicación.
"""
from app.core.logger import logger
from app.core.constants import ERROR_MESSAGES


class AppException(Exception):
    """
    Excepción base para toda la aplicación.
    Proporciona estructura consistente: código, mensaje, status_code, datos adicionales.
    """
    
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        data: dict = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.data = data or {}
        
        # Log de excepción (nivel depende del status_code)
        if status_code >= 500:
            logger.error(f"{code}: {message}", extra={"error_code": code})
        elif status_code >= 400:
            logger.warning(f"{code}: {message}", extra={"error_code": code})
        else:
            logger.info(f"{code}: {message}", extra={"error_code": code})
        
        super().__init__(self.message)


# ==============================================================================
# AUTENTICACIÓN Y AUTORIZACIÓN
# ==============================================================================

class UserNotFound(AppException):
    """Usuario no encontrado en base de datos."""
    def __init__(self):
        super().__init__(
            code="USER_NOT_FOUND",
            message=ERROR_MESSAGES["USER_NOT_FOUND"],
            status_code=404,
        )


class InvalidCredentials(AppException):
    """Credenciales (usuario/contraseña) inválidas."""
    def __init__(self):
        super().__init__(
            code="INVALID_CREDENTIALS",
            message=ERROR_MESSAGES["INVALID_CREDENTIALS"],
            status_code=401,
        )


class UserAlreadyExists(AppException):
    """Usuario ya existe (email o username duplicado)."""
    def __init__(self, field: str = "usuario"):
        super().__init__(
            code="USER_ALREADY_EXISTS",
            message=f"{field} ya está registrado",
            status_code=409,
            data={"field": field},
        )


class InvalidToken(AppException):
    """Token JWT inválido u expirado."""
    def __init__(self, reason: str = ""):
        msg = ERROR_MESSAGES.get("INVALID_TOKEN", "Token inválido u expirado")
        if reason:
            msg = f"{msg}: {reason}"
        
        super().__init__(
            code="INVALID_TOKEN",
            message=msg,
            status_code=401,
        )


class PermissionDenied(AppException):
    """Permiso denegado para acceder al recurso."""
    def __init__(self, reason: str = ""):
        msg = ERROR_MESSAGES.get("PERMISSION_DENIED", "Permiso denegado")
        if reason:
            msg = f"{msg}: {reason}"
        
        super().__init__(
            code="PERMISSION_DENIED",
            message=msg,
            status_code=403,
        )


class UserInactive(AppException):
    """Usuario está inactivo."""
    def __init__(self):
        super().__init__(
            code="USER_INACTIVE",
            message=ERROR_MESSAGES["USER_INACTIVE"],
            status_code=403,
        )


# ==============================================================================
# VALIDACIONES
# ==============================================================================

class ValidationError(AppException):
    """Error de validación general."""
    def __init__(self, field: str, message: str):
        super().__init__(
            code="VALIDATION_ERROR",
            message=f"Validación fallida en '{field}': {message}",
            status_code=422,
            data={"field": field},
        )


class WeakPassword(AppException):
    """Contraseña no cumple requisitos de seguridad."""
    def __init__(self):
        super().__init__(
            code="WEAK_PASSWORD",
            message=ERROR_MESSAGES["WEAK_PASSWORD"],
            status_code=422,
        )


class InvalidEmail(AppException):
    """Formato de email inválido."""
    def __init__(self):
        super().__init__(
            code="INVALID_EMAIL",
            message=ERROR_MESSAGES["INVALID_EMAIL"],
            status_code=422,
        )


class InvalidUsername(AppException):
    """Formato de username inválido."""
    def __init__(self):
        super().__init__(
            code="INVALID_USERNAME",
            message=ERROR_MESSAGES["INVALID_USERNAME"],
            status_code=422,
        )


# ==============================================================================
# RECURSOS
# ==============================================================================

class ResourceNotFound(AppException):
    """Recurso genérico no encontrado."""
    def __init__(self, resource_type: str = "Recurso"):
        super().__init__(
            code="RESOURCE_NOT_FOUND",
            message=f"{resource_type} no encontrado",
            status_code=404,
            data={"resource_type": resource_type},
        )


class ProductNotFound(AppException):
    """Producto no encontrado."""
    def __init__(self):
        super().__init__(
            code="PRODUCT_NOT_FOUND",
            message=ERROR_MESSAGES["PRODUCT_NOT_FOUND"],
            status_code=404,
        )


# ==============================================================================
# BASE DE DATOS
# ==============================================================================

class DatabaseError(AppException):
    """Error de base de datos."""
    def __init__(self, detail: str = ""):
        msg = ERROR_MESSAGES.get("DATABASE_ERROR", "Error de base de datos")
        if detail:
            msg = f"{msg}: {detail}"
        
        super().__init__(
            code="DATABASE_ERROR",
            message=msg,
            status_code=500,
        )


class RefreshTokenRevoked(AppException):
    """Refresh token ha sido revocado."""
    def __init__(self):
        super().__init__(
            code="REFRESH_TOKEN_REVOKED",
            message=ERROR_MESSAGES["REFRESH_TOKEN_REVOKED"],
            status_code=401,
        )
