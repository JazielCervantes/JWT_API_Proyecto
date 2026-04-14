// Cliente API - Maneja toda la comunicación con el backend
// 
// FASE 5 REFACTORING - SEGURIDAD MEJORADA:
// - Access token en sessionStorage (no persiste en reload, en memoria)
// - Refresh token en HTTP-Only cookie (servidor envía, JS no puede leer/modificar)
// - Retry automático con refresh en caso de 401
// - credentials: 'include' para enviar cookies

const API_URL = (import.meta.env.PUBLIC_API_URL || 'http://localhost:8000') + '/api/v1';

class APIClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.retryCount = 0;
    this.maxRetries = 1; // Solo 1 reintento para evitar loops infinitos
  }

  /**
   * Obtiene access token de sessionStorage (en memoria, no persiste).
   * 🔒 Seguro contra XSS porque no está en localStorage
   */
  getAccessToken() {
    if (typeof window === 'undefined') return null;
    return sessionStorage.getItem('access_token');
  }

  /**
   * El refresh token se obtiene automáticamente de la HTTP-Only cookie.
   * No necesitamos hacerlo manualmente - el navegador lo envía.
   * 🔒 HTTP-Only significa que JavaScript NO puede acceder, solo el servidor.
   */
  getRefreshToken() {
    // Ya no manualmente - HTTP-Only cookies se envían automáticamente
    return null;
  }

  /**
   * Guarda tokens de forma segura:
   * - Access token: sessionStorage (en memoria, se borra al cerrar pestaña)
   * - Refresh token: NO guardar (llega en HTTP-Only cookie del servidor)
   */
  saveTokens(accessToken, refreshToken) {
    if (typeof window === 'undefined') return;
    
    // ✅ Guardar solo el access token en sessionStorage
    // Se borra automáticamente cuando cierre la pestaña
    if (accessToken) {
      sessionStorage.setItem('access_token', accessToken);
    }
    
    // ❌ NO guardar refresh_token en storage
    // Llega en HTTP-Only cookie que el navegador envía automáticamente
    // El servidor maneja la rotación segura
  }

  async refreshAccessToken() {
    try {
      // 🔒 credentials: 'include' permite que se envíe la HTTP-Only cookie
      const response = await fetch(`${this.baseURL}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include', // ✅ Envía HTTP-Only refresh_token en cookie
        body: JSON.stringify({}), // Cuerpo vacío - token está en cookie
      });

      if (response.ok) {
        const data = await response.json();
        // ✅ Guardar nuevo access token
        this.saveTokens(data.access_token, null);
        this.retryCount = 0; // Reset contador
        return true;
      }

      // Si refresh falla (token expirado, revocado, etc.)
      if (response.status === 401 || response.status === 403) {
        this.clearAuth();
        return false;
      }

      return false;
    } catch (error) {
      console.error('Error refreshing token:', error);
      return false;
    }
  }

  clearAuth() {
    if (typeof window === 'undefined') return;
    sessionStorage.clear(); // Limpia sessionStorage
    localStorage.removeItem('user'); // Limpia user info
    // refresh_token en cookie se borra automáticamente por el servidor
    window.location.href = '/login';
  }

  async request(endpoint, options = {}) {
    const {
      requiresAuth = true,
      retryOnUnauth = true,
      ...fetchOptions
    } = options;

    const headers = {
      'Content-Type': 'application/json',
      ...fetchOptions.headers
    };

    // Agregar token de autenticación si es necesario
    if (requiresAuth) {
      const token = this.getAccessToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    // 🔒 credentials: 'include' para que las cookies se envíen automáticamente
    const fetchConfig = {
      ...fetchOptions,
      headers,
      credentials: 'include', // ✅ Envía HTTP-Only cookies
    };

    let response = await fetch(`${this.baseURL}${endpoint}`, fetchConfig);

    // Manejar 401 (Unauthorized) - token expirado
    if (response.status === 401 && requiresAuth && retryOnUnauth && this.retryCount < this.maxRetries) {
      this.retryCount++;
      const refreshed = await this.refreshAccessToken();

      if (refreshed) {
        // Reintentar request con nuevo token
        const newToken = this.getAccessToken();
        if (newToken) {
          headers['Authorization'] = `Bearer ${newToken}`;
        }
        response = await fetch(`${this.baseURL}${endpoint}`, {
          ...fetchConfig,
          headers,
        });
      } else {
        // Refresh falló - redirigir a login
        this.clearAuth();
        throw new Error('Sesión expirada. Por favor, inicia sesión nuevamente.');
      }
    }

    // Errores HTTP
    if (!response.ok) {
      const contentType = response.headers.get('content-type');
      let errorData;

      if (contentType && contentType.includes('application/json')) {
        errorData = await response.json().catch(() => ({}));
      } else {
        errorData = { error: 'ERROR_DESCONOCIDO' };
      }

      const errorMessage =
        errorData.message || errorData.detail || 'Error en la petición';

      const error = new Error(errorMessage);
      error.status = response.status;
      error.data = errorData;
      throw error;
    }

    // 204 No Content - no parsear JSON
    if (response.status === 204) return null;

    try {
      return await response.json();
    } catch {
      return null;
    }
  }

  // ── AUTH ──────────────────────────────────────
  /**
   * Login y obtener tokens
   * ✅ Access token → sessionStorage
   * ✅ Refresh token → HTTP-Only cookie (automático del servidor)
   */
  async login(username, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      requiresAuth: false,
      retryOnUnauth: false,
      body: JSON.stringify({ username, password }),
    });
    this.saveTokens(data.access_token, data.refresh_token);
    return data;
  }

  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      requiresAuth: false,
      retryOnUnauth: false,
      body: JSON.stringify(userData),
    });
  }

  async logout() {
    try {
      await this.request('/auth/logout', { method: 'POST' });
    } finally {
      // Limpiar sesión
      this.clearAuth();
    }
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }

  // ── PRODUCTS ──────────────────────────────────
  async getProducts(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') query.append(k, v);
    });
    return this.request(`/products?${query}`, { requiresAuth: false });
  }

  async getProduct(id) {
    return this.request(`/products/${id}`, { requiresAuth: false });
  }

  async createProduct(data) {
    return this.request('/products', { method: 'POST', body: JSON.stringify(data) });
  }

  async updateProduct(id, data) {
    return this.request(`/products/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  }

  async deleteProduct(id) {
    return this.request(`/products/${id}`, { method: 'DELETE' });
  }

  async getCategories() {
    return this.request('/products/categories/list', { requiresAuth: false });
  }

  // ── USERS (Admin) ─────────────────────────────
  async getUsers(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined) query.append(k, v);
    });
    return this.request(`/users?${query}`);
  }

  async updateUserRole(id, role) {
    return this.request(`/users/${id}/role`, {
      method: 'PATCH',
      body: JSON.stringify({ role }),
    });
  }

  async deleteUser(id) {
    return this.request(`/users/${id}`, { method: 'DELETE' });
  }

  async updateProfile(data) {
    return this.request('/auth/me', { method: 'PUT', body: JSON.stringify(data) });
  }

  async changePassword(currentPassword, newPassword) {
    return this.request('/auth/me/change-password', {
      method: 'POST',
      body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
    });
  }
}

export const api = new APIClient(API_URL);
export default api;
