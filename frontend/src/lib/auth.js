// Utilidades de autenticación en JavaScript puro

export function isAuthenticated() {
  if (typeof window === 'undefined') return false;
  return !!localStorage.getItem('access_token');
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
  if (typeof window !== 'undefined') localStorage.clear();
}

export function requireAuth() {
  if (typeof window === 'undefined') return;
  if (!isAuthenticated()) window.location.href = '/login';
}

export function requireAdmin() {
  if (typeof window === 'undefined') return;
  if (!isAuthenticated() || !isAdmin()) window.location.href = '/login';
}
