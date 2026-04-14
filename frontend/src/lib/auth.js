// Utilidades de autenticación en JavaScript puro
//
// FASE 5 REFACTORING - SEGURIDAD MEJORADA:
// - Access token: sessionStorage (elimina al cerrar pestaña)
// - Refresh token: HTTP-Only cookie (servidor lo maneja)
// - User data: localStorage (no-sensitivo, información de usuario)

/**
 * Verifica si el usuario está autenticado.
 * Busca en sessionStorage (prioridad) y localStorage (fallback).
 * sessionStorage es para esta sesión; localStorage es persistente entre pestañas.
 */
export function isAuthenticated() {
  if (typeof window === 'undefined') return false;
  // Probar primero sessionStorage (sesión actual)
  if (sessionStorage.getItem('access_token')) return true;
  // Fallback a localStorage (entre recargas/pestañas)
  if (localStorage.getItem('access_token')) return true;
  return false;
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
    sessionStorage.clear();
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
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
