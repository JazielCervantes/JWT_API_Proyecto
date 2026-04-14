# 🎨 Frontend - Astro + JavaScript Puro

Frontend moderno con tema **Dark Glass Morphism** construido con **Astro + JavaScript puro** (sin TypeScript).

## ✨ Características

### Diseño
- **Dark Glassmorphism** — tarjetas con blur y transparencia
- **Acentos Neón** — azul, púrpura, rosa, verde
- **Animaciones fluidas** — micro-interacciones suaves
- **Responsive** — funciona en mobile, tablet, desktop
- **Performance** — optimizado para velocidad

### Funcionalidades
- ✅ **Autenticación JWT** (login, registro, logout)
- ✅ **Gestión de tokens** (sessionStorage + HTTP-Only cookies)
- ✅ **Crud de productos** (solo admin)
- ✅ **Cuenta de usuario** (editar perfil, cambiar contraseña)
- ✅ **Dashboard** (estadísticas)
- ✅ **Toasts** notificaciones automáticas
- ✅ **Modales** para confirmaciones

## 🚀 Quick Start (3 minutos)

### Requisitos
- Node.js 18+ 
- Backend corriendo en http://localhost:8000

### Setup

```bash
cd frontend

# 1. Instalar dependencias
npm install

# 2. Configurar backend
cp .env.example .env
# Edita .env: PUBLIC_API_URL=http://localhost:8000

# 3. Iniciar desarrollo
npm run dev
```

✅ **Frontend en:** http://localhost:4321

## 📁 Estructura

```
frontend/
├── src/
│   ├── layouts/
│   │   └── Layout.astro              # Layout principal + toasts
│   ├── lib/
│   │   ├── api.js                    # Cliente API (fetch)
│   │   └── auth.js                   # Utilities de autenticación
│   ├── pages/                        # Rutas (Astro)
│   │   ├── index.astro               # Landing page
│   │   ├── login.astro               # Login
│   │   ├── register.astro            # Registro
│   │   ├── dashboard.astro           # Dashboard (auth)
│   │   ├── products.astro            # Catálogo productos
│   │   ├── profile.astro             # Perfil user
│   │   └── users.astro               # Gestión users (admin)
│   └── styles/
│       └── global.css                # TailwindCSS global
├── public/                           # Archivos estáticos
├── astro.config.mjs                  # Configuración Astro
├── tailwind.config.mjs               # Configuración Tailwind
└── package.json
```

## 📖 Páginas

| Página | URL | Autenticación | Descripción |
|--------|-----|---------------|-------------|
| **Landing** | `/` | Pública | Página de inicio |
| **Login** | `/login` | Pública | Iniciar sesión |
| **Registro** | `/register` | Pública | Crear cuenta |
| **Dashboard** | `/dashboard` | Usuario | Panel bienvenida |
| **Productos** | `/products` | Pública (CRUD: Admin) | Catálogo + gestión |
| **Perfil** | `/profile` | Usuario | Editar datos |
| **Usuarios** | `/users` | Admin | Gestión de usuarios |

## 🔧 Desarrollo

### Agregar Nueva Página

```astro
---
// src/pages/ejemplo.astro
import Layout from '../layouts/Layout.astro';
---

<Layout title="Mi Página">
  <h1>¡Hola!</h1>
</Layout>
```

### Llamar API

```javascript
// En un script de página .astro

import { api } from '../lib/api.js';

// Obtener datos
const users = await api.request('/users', {
  method: 'GET'
});
```

### Usar Auth

```javascript
import { isAuthenticated, clearAuth } from '../lib/auth.js';

if (!isAuthenticated()) {
  // Redirigir a login
  window.location.href = '/login';
}

// Logout
clearAuth();
```

## 🎨 Estilos

### Uso de TailwindCSS

```html
<!-- En archivos .astro -->
<button class="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded">
  Click
</button>
```

### Variables CSS Personalizadas

Ver `global.css` para:
- Colores (neón azul, púrpura, rosa, verde)
- Fuentes (Outfit, DM Sans)
- Spacings
- Velocidades de animación

## 🚀 Build & Deploy

### Build para Producción

```bash
npm run build
# Genera: dist/
```

### Preview Local

```bash
npm run preview
# Abre: http://localhost:4321
```

### Deploy a Vercel

```bash
# (Automático desde GitHub)
# Vercel detecta Astro automáticamente
```

Ver [docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md) para deploy completo.

## 📚 Tecnologías

| Tech | Versión | Propósito |
|------|---------|----------|
| **Astro** | 4+ | Framework SSG/SSR |
| **JavaScript** | ES2022 | Lógica del cliente |
| **TailwindCSS** | 3+ | Estilos |
| **Fetch API** | Nativo | HTTP requests |

**Sin TypeScript para máxima simplicity.**

## 🔐 Seguridad

- ✅ Access tokens en `sessionStorage` (se borra al cerrar)
- ✅ Refresh tokens en HTTP-Only cookies (automat)
- ✅ CSRF protection via SameSite
- ✅ Validación de datos en cliente

## 📊 Performance

- **Audits:** LightHouse 90+
- **Tamaño:** ~15KB JS (minified + gzipped)
- **Tiempo carga:** <1s en 4G

## ❓ FAQ

**P: ¿Por qué JavaScript en lugar de TypeScript?**
R: Máxima simplicidad y menos dependencias.

**P: ¿Por qué Astro?**
R: Mejor performance, SSG/SSR, integración con componentes.

**P: ¿Dónde está el localStorage?**
R: Usamos sessionStorage para tokens (mejor seguridad).

**P: ¿Puedo agregar componentes Vue/React?**
R: Sí, Astro soporta múltiples frameworks.

## 🔗 Links

- **Astro Docs**: https://astro.build
- **TailwindCSS Docs**: https://tailwindcss.com
- **Backend API**: [../docs/EXAMPLES.md](../docs/EXAMPLES.md)
- **Deploy**: [../docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md)

---

**Ver [INSTALLATION.md](../INSTALLATION.md) para setup completo del proyecto.**

