"""
Servicio de autenticación.
Lógica de negocio para registro, login y gestión de tokens.

⭐ FASE 3 REFACTORING:
- Usa UserRepository (inyección de dependencias)
- Reemplaza HTTPException con excepciones personalizadas
- Queries delegadas al repositorio
- Más testeable y mantenible
"""
<<<<<<< Updated upstream
from sqlalchemy.orm import Session
=======
>>>>>>> Stashed changes
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
)
from app.core.logger import logger
from app.utils.security import (
    verify_password,
    get_password_hash,
    create_tokens_for_user,
    decode_token
)
from app.core import (
    UserNotFound,
    InvalidCredentials,
    UserAlreadyExists,
    InvalidToken,
    UserInactive,
    RefreshTokenRevoked,
    logger,
)


class AuthService:
    """
    Servicio de autenticación.
<<<<<<< Updated upstream
    Maneja todas las operaciones relacionadas con autenticación.
    Utiliza excepciones personalizadas para manejo consistente de errores.
=======
    Maneja todas las operaciones relacionadas con auth.
    
    Pattern: inyección de dependencias del repositorio
    Se envía el repo desde las rutas para facilitar testing
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
            UserAlreadyExists: Si el email o username ya existen
        """
        # Verificar si el email ya existe
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            logger.warning(f"Intento de registro con email duplicado: {user_data.email}")
            raise UserAlreadyExists(field="Email")
        
        # Verificar si el username ya existe
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            logger.warning(f"Intento de registro con username duplicado: {user_data.username}")
            raise UserAlreadyExists(field="Username")
=======
            UserAlreadyExists: Si email o username ya existen
        """
        # Verificar email con repositorio
        if self.user_repo.email_exists(user_data.email):
            logger.warning(f"Intento de registro con email duplicado: {user_data.email}")
            raise UserAlreadyExists("Email")
        
        # Verificar username con repositorio
        if self.user_repo.username_exists(user_data.username):
            logger.warning(f"Intento de registro con username duplicado: {user_data.username}")
            raise UserAlreadyExists("Username")
>>>>>>> Stashed changes
        
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
        
        logger.info(f"Nuevo usuario registrado: {user_data.username} ({user_data.email})")
        
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
<<<<<<< Updated upstream
            InvalidCredentials: Si las credenciales son incorrectas
=======
            InvalidCredentials: Si el usuario no existe o contraseña es incorrecta
>>>>>>> Stashed changes
            UserInactive: Si el usuario está inactivo
        """
        # Buscar usuario por email o username con repositorio
        user = self.user_repo.get_by_email_or_username(username)
        
        if not user:
<<<<<<< Updated upstream
            logger.warning(f"Intento de login con usuario no encontrado: {username}")
=======
            logger.warning(f"Intento fallido de login: usuario no encontrado ({username})")
>>>>>>> Stashed changes
            raise InvalidCredentials()
        
        # Verificar contraseña
        if not verify_password(password, user.hashed_password):
<<<<<<< Updated upstream
            logger.warning(f"Intento de login con contraseña incorrecta: {username}")
=======
            logger.warning(f"Intento fallido de login: contraseña incorrecta ({username})")
>>>>>>> Stashed changes
            raise InvalidCredentials()
        
        # Verificar que el usuario esté activo
        if not user.is_active:
            logger.warning(f"Intento de login con usuario inactivo: {username}")
            raise UserInactive()
<<<<<<< Updated upstream
=======
        
        logger.info(f"Autenticación exitosa: {username}", extra={"user_id": user.id})
>>>>>>> Stashed changes
        
        logger.info(f"Usuario autenticado: {username}")
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
<<<<<<< Updated upstream
        # Autenticar usuario (puede lanzar InvalidCredentials o UserInactive)
        user = AuthService.authenticate_user(db, username, password)
=======
        # Autenticar usuario
        user = self.authenticate_user(username, password)
>>>>>>> Stashed changes
        
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
        
        logger.info(f"Login exitoso: {username}")
        
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
<<<<<<< Updated upstream
            InvalidToken: Si el refresh token es inválido
            RefreshTokenRevoked: Si el refresh token fue revocado
=======
            InvalidToken: Si el refresh token es inválido/expirado
            UserNotFound: Si el usuario no existe
>>>>>>> Stashed changes
        """
        # Decodificar refresh token
        payload = decode_token(refresh_token)
        
        if payload is None:
<<<<<<< Updated upstream
            logger.warning("Intento de refresh con token inválido o expirado")
            raise InvalidToken(reason="Token expirado o inválido")
=======
            logger.warning("Intento de refresh con token expirado/inválido")
            raise InvalidToken("Token expirado")
>>>>>>> Stashed changes
        
        # Verificar que sea un refresh token
        if payload.get("token_type") != "refresh":
            logger.warning("Intento de refresh con tipo de token incorrecto")
<<<<<<< Updated upstream
            raise InvalidToken(reason="Tipo de token incorrecto")
        
        user_id = payload.get("user_id")
        if user_id is None:
            logger.warning("Refresh token sin user_id")
            raise InvalidToken()
=======
            raise InvalidToken("Tipo de token inválido para refresh")
        
        user_id = payload.get("user_id")
        if user_id is None:
            raise InvalidToken("Token malformado")
>>>>>>> Stashed changes
        
        # Buscar usuario con repositorio
        user = self.user_repo.get_by_id(user_id)
        
<<<<<<< Updated upstream
        if not user:
            logger.warning(f"Refresh: Usuario no encontrado (ID: {user_id})")
            raise UserNotFound()
        
        if not user.is_active:
            logger.warning(f"Refresh: Usuario inactivo (ID: {user_id})")
            raise UserInactive()
        
        # Verificar que el refresh token coincida con el guardado (revocation check)
        if user.refresh_token != refresh_token:
            logger.warning(f"Refresh: Token revocado o no coincide (user: {user.username})")
=======
        if not user or not user.is_active:
            logger.warning(f"Intento de refresh con usuario no encontrado/inactivo: {user_id}")
            raise UserInactive()
        
        # Verificar que el refresh token coincida con el guardado (prevenir reutilización)
        if user.refresh_token != refresh_token:
            logger.warning(f"Intento de refresh con token desincronizado (usuario: {user_id})")
>>>>>>> Stashed changes
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
        
        logger.info(f"Token refrescado: {user.username}")
        
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
<<<<<<< Updated upstream
        user.refresh_token = None
        db.commit()
        
        logger.info(f"Logout: {user.username}")
=======
        # Limpiar refresh token (soft invalidation)
        user_update_data = {"refresh_token": None}
        self.user_repo.update(user.id, user_update_data)
        
        logger.info(f"Logout: {user.username}", extra={"user_id": user.id})
>>>>>>> Stashed changes
