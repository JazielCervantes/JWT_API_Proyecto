// Cliente API - Maneja toda la comunicación con el backend
// Escrito en JavaScript puro (sin TypeScript)

const API_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

class APIClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  getAccessToken() {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  }

  getRefreshToken() {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('refresh_token');
  }

  saveTokens(accessToken, refreshToken) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  }

  async refreshAccessToken() {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) return false;
    try {
      const response = await fetch(`${this.baseURL}/api/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });
      if (response.ok) {
        const data = await response.json();
        this.saveTokens(data.access_token, data.refresh_token);
        return true;
      }
      return false;
    } catch {
      return false;
    }
  }

  async request(endpoint, options = {}) {
    const { requiresAuth = true, ...fetchOptions } = options;
    const headers = { 'Content-Type': 'application/json', ...fetchOptions.headers };
    if (requiresAuth) {
      const token = this.getAccessToken();
      if (token) headers['Authorization'] = `Bearer ${token}`;
    }

    let response = await fetch(`${this.baseURL}${endpoint}`, { ...fetchOptions, headers });

    if (response.status === 401 && requiresAuth) {
      const refreshed = await this.refreshAccessToken();
      if (refreshed) {
        const newToken = this.getAccessToken();
        if (newToken) headers['Authorization'] = `Bearer ${newToken}`;
        response = await fetch(`${this.baseURL}${endpoint}`, { ...fetchOptions, headers });
      } else {
        if (typeof window !== 'undefined') {
          localStorage.clear();
          window.location.href = '/login';
        }
        throw new Error('Sesión expirada');
      }
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Error desconocido' }));
      throw new Error(error.detail || 'Error en la petición');
    }

    // 204 No Content - no parsear JSON
    if (response.status === 204) return null;
    return response.json();
  }

  // ── AUTH ──────────────────────────────────────
  async login(username, password) {
    const data = await this.request('/api/auth/login', {
      method: 'POST',
      requiresAuth: false,
      body: JSON.stringify({ username, password }),
    });
    this.saveTokens(data.access_token, data.refresh_token);
    return data;
  }

  async register(userData) {
    return this.request('/api/auth/register', {
      method: 'POST',
      requiresAuth: false,
      body: JSON.stringify(userData),
    });
  }

  async logout() {
    try {
      await this.request('/api/auth/logout', { method: 'POST' });
    } finally {
      if (typeof window !== 'undefined') {
        localStorage.clear();
        window.location.href = '/login';
      }
    }
  }

  async getCurrentUser() {
    return this.request('/api/users/me');
  }

  // ── PRODUCTS ──────────────────────────────────
  async getProducts(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') query.append(k, v);
    });
    return this.request(`/api/products?${query}`, { requiresAuth: false });
  }

  async getProduct(id) {
    return this.request(`/api/products/${id}`, { requiresAuth: false });
  }

  async createProduct(data) {
    return this.request('/api/products', { method: 'POST', body: JSON.stringify(data) });
  }

  async updateProduct(id, data) {
    return this.request(`/api/products/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  }

  async deleteProduct(id) {
    return this.request(`/api/products/${id}`, { method: 'DELETE' });
  }

  async getCategories() {
    return this.request('/api/products/categories/list', { requiresAuth: false });
  }

  // ── USERS (Admin) ─────────────────────────────
  async getUsers(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined) query.append(k, v);
    });
    return this.request(`/api/users?${query}`);
  }

  async updateUserRole(id, role) {
    return this.request(`/api/users/${id}/role`, {
      method: 'PATCH',
      body: JSON.stringify({ role }),
    });
  }

  async deleteUser(id) {
    return this.request(`/api/users/${id}`, { method: 'DELETE' });
  }

  async updateProfile(data) {
    return this.request('/api/users/me', { method: 'PUT', body: JSON.stringify(data) });
  }

  async changePassword(currentPassword, newPassword) {
    return this.request('/api/users/me/change-password', {
      method: 'POST',
      body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
    });
  }
}

export const api = new APIClient(API_URL);
export default api;
