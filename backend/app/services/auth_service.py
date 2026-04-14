"""
Servicio de autenticación.
Lógica de negocio para registro, login y gestión de tokens.

⭐ FASE 3 REFACTORING:
- Usa UserRepository (inyección de dependencias)
- Reemplaza HTTPException con excepciones personalizadas
- Queries delegadas al repositorio
- Más testeable y mantenible
"""
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.schemas.auth import TokenResponse
from app.core.exceptions import (
    UserAlreadyExists,
    InvalidCredentials,
    InvalidToken,
    UserInactive,
    RefreshTokenRevoked,
    UserNotFound,
)
from app.core.logger import logger
from app.utils.security import (
    verify_password,
    get_password_hash,
    create_tokens_for_user,
    decode_token
)


class AuthService:
    """
    Servicio de autenticación.
    Maneja todas las operaciones relacionadas con autenticación.
    Utiliza excepciones personalizadas para manejo consistente de errores.
    
    Pattern: inyección de dependencias del repositorio
    Se envía el repo desde las rutas para facilitar testing
    """
    
    def __init__(self, user_repository: UserRepository):
        """
        Inicializa el servicio con inyección de repositorio.
        
        Args:
            user_repository: Instancia de UserRepository
        """
        self.user_repo = user_repository
    
    def register_user(self, user_data: UserCreate) -> User:
        """
        Registra un nuevo usuario.
        
        Args:
            user_data: Datos del usuario a crear
        
        Returns:
            Usuario creado
        
        Raises:
            UserAlreadyExists: Si el email o username ya existen
        """
        # Verificar email con repositorio
        if self.user_repo.email_exists(user_data.email):
            logger.warning(f"Intento de registro con email duplicado: {user_data.email}")
            raise UserAlreadyExists("Email")
        
        # Verificar username con repositorio
        if self.user_repo.username_exists(user_data.username):
            logger.warning(f"Intento de registro con username duplicado: {user_data.username}")
            raise UserAlreadyExists("Username")
        
        # Crear nuevo usuario
        hashed_password = get_password_hash(user_data.password)
        
        new_user_data = {
            "email": user_data.email,
            "username": user_data.username,
            "full_name": user_data.full_name,
            "hashed_password": hashed_password,
            "role": UserRole.USER,
            "is_active": True
        }
        
        # Usar repositorio para crear
        new_user = self.user_repo.create(new_user_data)
        
        logger.info(f"Usuario registrado exitosamente: {new_user.username}", 
                   extra={"user_id": new_user.id})
        
        return new_user
    
    def authenticate_user(self, username: str, password: str) -> User:
        """
        Autentica un usuario con username/email y contraseña.
        
        Args:
            username: Username o email del usuario
            password: Contraseña en texto plano
        
        Returns:
            Usuario autenticado
        
        Raises:
            InvalidCredentials: Si las credenciales son incorrectas
            UserInactive: Si el usuario está inactivo
        """
        # Buscar usuario por email o username con repositorio
        user = self.user_repo.get_by_email_or_username(username)
        
        if not user:
            logger.warning(f"Intento fallido de login: usuario no encontrado ({username})")
            raise InvalidCredentials()
        
        # Verificar contraseña
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Intento fallido de login: contraseña incorrecta ({username})")
            raise InvalidCredentials()
        
        # Verificar que el usuario esté activo
        if not user.is_active:
            logger.warning(f"Intento de login con usuario inactivo: {username}")
            raise UserInactive()
        
        logger.info(f"Autenticación exitosa: {username}", extra={"user_id": user.id})
        return user
    
    def login(self, username: str, password: str) -> TokenResponse:
        """
        Realiza el login y genera tokens.
        
        Args:
            username: Username o email
            password: Contraseña
        
        Returns:
            Respuesta con access y refresh tokens
        
        Raises:
            InvalidCredentials, UserInactive
        """
        # Autenticar usuario
        user = self.authenticate_user(username, password)
        
        # Generar tokens
        access_token, refresh_token = create_tokens_for_user(
            user.id,
            user.username,
            user.role
        )
        
        # Actualizar refresh token en BD (para poder invalidarlo después)
        user_update_data = {"refresh_token": refresh_token}
        self.user_repo.update(user.id, user_update_data)
        
        logger.info(f"Login exitoso: {user.username}", extra={"user_id": user.id})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """
        Genera un nuevo access token usando un refresh token.
        
        Args:
            refresh_token: Refresh token válido
        
        Returns:
            Nueva respuesta con tokens
        
        Raises:
            InvalidToken: Si el refresh token es inválido
            RefreshTokenRevoked: Si el refresh token fue revocado
            UserNotFound: Si el usuario no existe
        """
        # Decodificar refresh token
        payload = decode_token(refresh_token)
        
        if payload is None:
            logger.warning("Intento de refresh con token inválido o expirado")
            raise InvalidToken("Token expirado o inválido")
        
        # Verificar que sea un refresh token
        if payload.get("token_type") != "refresh":
            logger.warning("Intento de refresh con tipo de token incorrecto")
            raise InvalidToken("Tipo de token incorrecto")
        
        user_id = payload.get("user_id")
        if user_id is None:
            logger.warning("Refresh token sin user_id")
            raise InvalidToken()
        
        # Buscar usuario con repositorio
        user = self.user_repo.get_by_id(user_id)
        
        if not user:
            logger.warning(f"Refresh: Usuario no encontrado (ID: {user_id})")
            raise UserNotFound()
        
        if not user.is_active:
            logger.warning(f"Refresh: Usuario inactivo (ID: {user_id})")
            raise UserInactive()
        
        # Verificar que el refresh token coincida con el guardado (revocation check)
        if user.refresh_token != refresh_token:
            logger.warning(f"Refresh: Token revocado o no coincide (user: {user.username})")
            raise RefreshTokenRevoked()
        
        # Generar nuevos tokens
        access_token, new_refresh_token = create_tokens_for_user(
            user.id,
            user.username,
            user.role
        )
        
        # Actualizar refresh token en BD
        user_update_data = {"refresh_token": new_refresh_token}
        self.user_repo.update(user.id, user_update_data)
        
        logger.info(f"Refresh token exitoso: {user.username}", extra={"user_id": user.id})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
    
    def logout(self, user: User) -> None:
        """
        Cierra sesión invalidando el refresh token.
        
        Args:
            user: Usuario actual
        """
        # Limpiar refresh token (soft invalidation)
        user_update_data = {"refresh_token": None}
        self.user_repo.update(user.id, user_update_data)
        
        logger.info(f"Logout: {user.username}", extra={"user_id": user.id})
