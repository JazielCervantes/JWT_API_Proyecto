// Utilidades de autenticación en JavaScript puro
//
// FASE 5 REFACTORING - SEGURIDAD MEJORADA:
// - Access token: sessionStorage (elimina al cerrar pestaña)
// - Refresh token: HTTP-Only cookie (servidor lo maneja)
// - User data: localStorage (no-sensitivo, información de usuario)

/**
 * Verifica si el usuario está autenticado.
 * Revisa sessionStorage para el access token.
 */
export function isAuthenticated() {
  if (typeof window === 'undefined') return false;
  return !!sessionStorage.getItem('access_token');
}

export function getUser() {
  if (typeof window === 'undefined') return null;
  try {
    return JSON.parse(localStorage.getItem('user') || 'null');
  } catch {
    return null;
  }
}

export function saveUser(user) {
  if (typeof window === 'undefined') return;
  localStorage.setItem('user', JSON.stringify(user));
}

export function isAdmin() {
  return getUser()?.role === 'admin';
}

export function clearAuth() {
  if (typeof window !== 'undefined') {
    sessionStorage.clear(); // Limpia sessionStorage (access token)
    localStorage.removeItem('user'); // Limpia datos del usuario
    // refresh_token en HTTP-Only cookie se borra automáticamente por servidor
  }
}

export function requireAuth() {
  if (typeof window === 'undefined') return;
  if (!isAuthenticated()) window.location.href = '/login';
}

export function requireAdmin() {
  if (typeof window === 'undefined') return;
  if (!isAuthenticated() || !isAdmin()) window.location.href = '/login';
}
