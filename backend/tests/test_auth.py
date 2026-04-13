"""
Tests para excepciones personalizadas.
Verifica que los códigos de error y mensajes sean consistentes.
"""
import pytest
from app.core.exceptions import (
    UserNotFound,
    InvalidCredentials,
    UserAlreadyExists,
    InvalidToken,
    PermissionDenied,
    UserInactive,
    WeakPassword,
    RefreshTokenRevoked,
)


class TestAppExceptions:
    """Suite de tests para excepciones personalizadas."""
    
    def test_user_not_found_exception(self):
        """UserNotFound retorna código 404."""
        exc = UserNotFound()
        assert exc.code == "USER_NOT_FOUND"
        assert exc.status_code == 404
        assert "no encontrado" in exc.message.lower()
    
    def test_invalid_credentials_exception(self):
        """InvalidCredentials retorna código 401."""
        exc = InvalidCredentials()
        assert exc.code == "INVALID_CREDENTIALS"
        assert exc.status_code == 401
    
    def test_user_already_exists_exception(self):
        """UserAlreadyExists retorna código 409."""
        exc = UserAlreadyExists(field="email")
        assert exc.code == "USER_ALREADY_EXISTS"
        assert exc.status_code == 409
        assert exc.data["field"] == "email"
    
    def test_invalid_token_exception(self):
        """InvalidToken retorna código 401."""
        exc = InvalidToken(reason="Token expirado")
        assert exc.code == "INVALID_TOKEN"
        assert exc.status_code == 401
        assert "Token expirado" in exc.message
    
    def test_permission_denied_exception(self):
        """PermissionDenied retorna código 403."""
        exc = PermissionDenied(reason="Admin required")
        assert exc.code == "PERMISSION_DENIED"
        assert exc.status_code == 403
        assert "Admin required" in exc.message
    
    def test_user_inactive_exception(self):
        """UserInactive retorna código 403."""
        exc = UserInactive()
        assert exc.code == "USER_INACTIVE"
        assert exc.status_code == 403
    
    def test_weak_password_exception(self):
        """WeakPassword retorna código 422."""
        exc = WeakPassword()
        assert exc.code == "WEAK_PASSWORD"
        assert exc.status_code == 422
    
    def test_refresh_token_revoked_exception(self):
        """RefreshTokenRevoked retorna código 401."""
        exc = RefreshTokenRevoked()
        assert exc.code == "REFRESH_TOKEN_REVOKED"
        assert exc.status_code == 401


class TestAuthenticationFlow:
    """Suite de tests para el flujo de autenticación."""
    
    def test_register_success(self, client, sample_user_data):
        """Registro exitoso retorna usuario creado."""
        response = client.post("/api/auth/register", json=sample_user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == sample_user_data["username"]
        assert data["email"] == sample_user_data["email"]
        assert data["role"] == "user"
    
    def test_register_duplicate_email(self, client, sample_user_data):
        """Registrase con email duplicado retorna error 409."""
        # Primer registro exitoso
        response1 = client.post("/api/auth/register", json=sample_user_data)
        assert response1.status_code == 201
        
        # Segundo registro con mismo email debe fallar
        response2 = client.post("/api/auth/register", json={
            **sample_user_data,
            "username": "different_username"
        })
        assert response2.status_code == 409
        data = response2.json()
        assert data["error"] == "USER_ALREADY_EXISTS"
    
    def test_register_duplicate_username(self, client, sample_user_data):
        """Registrase con username duplicado retorna error 409."""
        # Primer registro exitoso
        response1 = client.post("/api/auth/register", json=sample_user_data)
        assert response1.status_code == 201
        
        # Segundo registro con mismo username debe fallar
        response2 = client.post("/api/auth/register", json={
            **sample_user_data,
            "email": "different@example.com"
        })
        assert response2.status_code == 409
        data = response2.json()
        assert data["error"] == "USER_ALREADY_EXISTS"
    
    def test_login_success(self, client, sample_user_data):
        """Login exitoso retorna tokens."""
        # Registrar usuario
        client.post("/api/auth/register", json=sample_user_data)
        
        # Login
        response = client.post("/api/auth/login", json={
            "username": sample_user_data["username"],
            "password": sample_user_data["password"]
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_username(self, client):
        """Login con usuario inexistente retorna 401."""
        response = client.post("/api/auth/login", json={
            "username": "nonexistent",
            "password": "SomePass123!"
        })
        assert response.status_code == 401
        data = response.json()
        assert data["error"] == "INVALID_CREDENTIALS"
    
    def test_login_invalid_password(self, client, sample_user_data):
        """Login con contraseña incorrecta retorna 401."""
        # Registrar usuario
        client.post("/api/auth/register", json=sample_user_data)
        
        # Login con contraseña incorrecta
        response = client.post("/api/auth/login", json={
            "username": sample_user_data["username"],
            "password": "WrongPass123!"
        })
        assert response.status_code == 401
        data = response.json()
        assert data["error"] == "INVALID_CREDENTIALS"
    
    def test_get_me_with_token(self, client, sample_user_data):
        """GET /me con token válido retorna usuario."""
        # Registrar
        client.post("/api/auth/register", json=sample_user_data)
        
        # Login
        login_response = client.post("/api/auth/login", json={
            "username": sample_user_data["username"],
            "password": sample_user_data["password"]
        })
        access_token = login_response.json()["access_token"]
        
        # Get me
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == sample_user_data["username"]
    
    def test_get_me_without_token(self, client):
        """GET /me sin token retorna 403."""
        response = client.get("/api/auth/me")
        assert response.status_code == 403  # No credentials provided
    
    def test_refresh_token_success(self, client, sample_user_data):
        """Refresh token exitoso retorna nuevo access_token."""
        # Registrar
        client.post("/api/auth/register", json=sample_user_data)
        
        # Login
        login_response = client.post("/api/auth/login", json={
            "username": sample_user_data["username"],
            "password": sample_user_data["password"]
        })
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh
        response = client.post("/api/auth/refresh", json={
            "refresh_token": refresh_token
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
    
    def test_refresh_token_invalid(self, client):
        """Refresh con token inválido retorna 401."""
        response = client.post("/api/auth/refresh", json={
            "refresh_token": "invalid_token_here"
        })
        assert response.status_code == 401
        data = response.json()
        assert data["error"] == "INVALID_TOKEN"
    
    def test_logout_success(self, client, sample_user_data):
        """Logout exitoso invalida el refresh token."""
        # Registrar
        client.post("/api/auth/register", json=sample_user_data)
        
        # Login
        login_response = client.post("/api/auth/login", json={
            "username": sample_user_data["username"],
            "password": sample_user_data["password"]
        })
        access_token = login_response.json()["access_token"]
        refresh_token = login_response.json()["refresh_token"]
        
        # Logout
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        
        # Intentar refresh después del logout - debe fallar
        response = client.post("/api/auth/refresh", json={
            "refresh_token": refresh_token
        })
        assert response.status_code == 401
        data = response.json()
        assert data["error"] == "REFRESH_TOKEN_REVOKED"
