# Frontend

Construido con Astro 4, Vue 3 y TailwindCSS. Diseño minimalista inspirado en herramientas SaaS modernas como Vercel o Linear.

## Características

- Modo claro y oscuro con persistencia en localStorage
- Command palette con Ctrl+K para navegación rápida
- Sidebar fijo en desktop, colapsable en mobile
- Skeleton loaders en todas las vistas con datos remotos
- Gestión de tokens JWT con retry automático en 401

## Páginas

| Ruta | Descripción | Acceso |
|---|---|---|
| `/` | Landing page | Público |
| `/login` | Inicio de sesión | Público |
| `/register` | Registro de cuenta | Público |
| `/dashboard` | Panel principal con estadísticas | Autenticado |
| `/products` | CRUD de productos con búsqueda y paginación | Autenticado |
| `/users` | Gestión de usuarios con roles | Solo admin |
| `/profile` | Editar perfil y cambiar contraseña | Autenticado |

## Setup local

Necesitas Node.js 18+ y el backend corriendo en localhost:8000.

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

La variable `PUBLIC_API_URL` en `.env` debe apuntar al backend:

```env
# Local
PUBLIC_API_URL=http://localhost:8000

# Producción (Vercel)
PUBLIC_API_URL=https://tu-backend.railway.app
```

## Estructura

```
src/
├── components/
│   ├── layout/
│   │   └── CommandPalette.vue   # Paleta de comandos (Ctrl+K)
│   └── ui/
│       └── ThemeToggle.vue      # Toggle modo claro/oscuro
├── layouts/
│   ├── Layout.astro             # Páginas públicas (login, registro)
│   └── DashboardLayout.astro   # Páginas autenticadas (sidebar + navbar)
├── lib/
│   ├── api.js                   # Cliente HTTP con retry automático
│   └── auth.js                  # Utilidades de sesión y redirección
├── pages/
│   ├── index.astro
│   ├── login.astro
│   ├── register.astro
│   ├── dashboard.astro
│   ├── products.astro
│   ├── users.astro
│   └── profile.astro
└── styles/
    └── global.css
```

## Build de producción

```bash
npm run build    # Genera /dist
npm run preview  # Preview local del build
```

El output es completamente estático (`output: 'static'`), listo para Vercel sin ninguna configuración adicional de servidor.
