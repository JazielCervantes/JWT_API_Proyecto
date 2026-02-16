"""
Servicio de autenticación.
Lógica de negocio para registro, login y gestión de tokens.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.schemas.auth import TokenResponse
from app.utils.security import (
    verify_password,
    get_password_hash,
    create_tokens_for_user,
    decode_token
)


class AuthService:
    """
    Servicio de autenticación.
    Maneja todas las operaciones relacionadas con auth.
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
            HTTPException: Si el email o username ya existen
        """
        # Verificar si el email ya existe
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Verificar si el username ya existe
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El username ya está en uso"
            )
        
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
            HTTPException: Si las credenciales son incorrectas
        """
        # Buscar por username o email
        user = db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar contraseña
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar que el usuario esté activo
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
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
        # Autenticar usuario
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
            HTTPException: Si el refresh token es inválido
        """
        # Decodificar refresh token
        payload = decode_token(refresh_token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado"
            )
        
        # Verificar que sea un refresh token
        if payload.get("token_type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tipo de token inválido"
            )
        
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        # Buscar usuario
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado o inactivo"
            )
        
        # Verificar que el refresh token coincida con el guardado
        if user.refresh_token != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido"
            )
        
        # Generar nuevos tokens
        access_token, new_refresh_token = create_tokens_for_user(
            user.id,
            user.username,
            user.role
        )
        
        # Actualizar refresh token en BD
        user.refresh_token = new_refresh_token
        db.commit()
        
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
