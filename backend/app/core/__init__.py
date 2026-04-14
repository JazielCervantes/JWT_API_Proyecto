"""
Core module - Cross-cutting concerns.
Contiene logging, excepciones y constantes globales.
"""
from app.core.logger import logger
from app.core.exceptions import (
    AppException,
    UserNotFound,
    InvalidCredentials,
    UserAlreadyExists,
    InvalidToken,
    PermissionDenied,
    UserInactive,
    ValidationError as AppValidationError,
    ResourceNotFound,
    ProductNotFound,
    RefreshTokenRevoked,
    WeakPassword,
    DatabaseError,
)

__all__ = [
    "logger",
    "AppException",
    "UserNotFound",
    "InvalidCredentials",
    "UserAlreadyExists",
    "InvalidToken",
    "PermissionDenied",
    "UserInactive",
    "AppValidationError",
    "ResourceNotFound",
    "ProductNotFound",
    "RefreshTokenRevoked",
    "WeakPassword",
    "DatabaseError",
]
