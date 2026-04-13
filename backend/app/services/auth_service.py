"""
Servicio de autenticación.
Lógica de negocio para registro, login y gestión de tokens.
"""
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.schemas.auth import TokenResponse
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
    Maneja todas las operaciones relacionadas con autenticación.
    Utiliza excepciones personalizadas para manejo consistente de errores.
    """
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """
        Registra un nuevo usuario.
        
        Args:
            db: Sesión de base de datos
            user_data: Datos del usuario a crear
        
        Returns:
            Usuario creado
        
        Raises:
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
        
        # Crear nuevo usuario
        hashed_password = get_password_hash(user_data.password)
        
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            role=UserRole.USER,  # Por defecto es usuario normal
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"Nuevo usuario registrado: {user_data.username} ({user_data.email})")
        
        return new_user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """
        Autentica un usuario con username/email y contraseña.
        
        Args:
            db: Sesión de base de datos
            username: Username o email del usuario
            password: Contraseña en texto plano
        
        Returns:
            Usuario autenticado
        
        Raises:
            InvalidCredentials: Si las credenciales son incorrectas
            UserInactive: Si el usuario está inactivo
        """
        # Buscar por username o email
        user = db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user:
            logger.warning(f"Intento de login con usuario no encontrado: {username}")
            raise InvalidCredentials()
        
        # Verificar contraseña
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Intento de login con contraseña incorrecta: {username}")
            raise InvalidCredentials()
        
        # Verificar que el usuario esté activo
        if not user.is_active:
            logger.warning(f"Intento de login con usuario inactivo: {username}")
            raise UserInactive()
        
        logger.info(f"Usuario autenticado: {username}")
        return user
    
    @staticmethod
    def login(db: Session, username: str, password: str) -> TokenResponse:
        """
        Realiza el login y genera tokens.
        
        Args:
            db: Sesión de base de datos
            username: Username o email
            password: Contraseña
        
        Returns:
            Respuesta con access y refresh tokens
        """
        # Autenticar usuario (puede lanzar InvalidCredentials o UserInactive)
        user = AuthService.authenticate_user(db, username, password)
        
        # Generar tokens
        access_token, refresh_token = create_tokens_for_user(
            user.id,
            user.username,
            user.role
        )
        
        # Guardar refresh token en la BD (para poder invalidarlo después)
        user.refresh_token = refresh_token
        db.commit()
        
        logger.info(f"Login exitoso: {username}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> TokenResponse:
        """
        Genera un nuevo access token usando un refresh token.
        
        Args:
            db: Sesión de base de datos
            refresh_token: Refresh token válido
        
        Returns:
            Nueva respuesta con tokens
        
        Raises:
            InvalidToken: Si el refresh token es inválido
            RefreshTokenRevoked: Si el refresh token fue revocado
        """
        # Decodificar refresh token
        payload = decode_token(refresh_token)
        
        if payload is None:
            logger.warning("Intento de refresh con token inválido o expirado")
            raise InvalidToken(reason="Token expirado o inválido")
        
        # Verificar que sea un refresh token
        if payload.get("token_type") != "refresh":
            logger.warning("Intento de refresh con tipo de token incorrecto")
            raise InvalidToken(reason="Tipo de token incorrecto")
        
        user_id = payload.get("user_id")
        if user_id is None:
            logger.warning("Refresh token sin user_id")
            raise InvalidToken()
        
        # Buscar usuario
        user = db.query(User).filter(User.id == user_id).first()
        
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
        user.refresh_token = new_refresh_token
        db.commit()
        
        logger.info(f"Token refrescado: {user.username}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
    
    @staticmethod
    def logout(db: Session, user: User) -> None:
        """
        Cierra sesión invalidando el refresh token.
        
        Args:
            db: Sesión de base de datos
            user: Usuario actual
        """
        user.refresh_token = None
        db.commit()
        
        logger.info(f"Logout: {user.username}")
