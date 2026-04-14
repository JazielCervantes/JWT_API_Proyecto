"""
Middleware de seguridad.
Rate limiting + Security headers + CORS protegido.
"""
from fastapi import Request, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.core import logger


# Configurar limiter
limiter = Limiter(key_func=get_remote_address)


async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    """
    Manejador personalizado para excepciones de rate limit.
    """
    logger.warning(
        f"Rate limit exceeded for {request.method} {request.url.path}",
        extra={"ip": request.client.host if request.client else "unknown"}
    )
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "RATE_LIMIT_EXCEEDED",
            "message": "Demasiadas solicitudes. Intenta más tarde.",
            "retry_after": 60
        }
    )


async def security_headers_middleware(request: Request, call_next):
    """
    Middleware que agrega headers de seguridad a todas las responses.
    Protege contra: MIME sniffing, clickjacking, XSS, CSRF, etc.
    
    Notas:
    - Las rutas /docs, /redoc y /openapi.json tienen CSP permisivo (permiten CDN)
    - El resto de rutas tienen CSP restrictivo
    """
    response = await call_next(request)
    
    # Previene MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # Clickjacking protection
    response.headers["X-Frame-Options"] = "DENY"
    
    # XSS protection (legacy, Chrome ya no lo usa pero otros navegadores sí)
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # HTTPS only (HSTS) - máximo 1 año
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    
    # Content Security Policy - adaptado según la ruta
    # Las rutas de documentación necesitan acceso a CDN para Swagger UI
    if request.url.path in ["/docs", "/redoc", "/openapi.json"] or \
       request.url.path.startswith("/docs") or \
       request.url.path.startswith("/redoc") or \
       request.url.path.startswith("/openapi"):
        # CSP permisivo para documentación (requiere CDN)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self' https:; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net https://unpkg.com; "
            "connect-src 'self' https:"
        )
    else:
        # CSP restrictivo para el resto de rutas
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'"
        )
    
    # Referrer Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Permissions Policy (antes Feature-Policy) - deshabilita features innecesarias
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    return response
