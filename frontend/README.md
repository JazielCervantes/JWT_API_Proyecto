# 🎨 Frontend Nexus — Dark Glass UI

Frontend moderno con tema Dark Glass Morphism construido con **Astro + JavaScript puro** (sin TypeScript).

## ✨ Características de Diseño

- **Dark Glassmorphism** — tarjetas con blur y transparencia
- **Acentos Neón** — azul (#00D4FF), púrpura (#9B5CFF), rosa (#FF2D9B), verde (#00FF88)
- **Fuentes únicas** — Outfit (display) + DM Sans (body)
- **Animaciones fluidas** — micro-interacciones en botones, cards y formularios
- **Toasts interactivos** — notificaciones de éxito/error
- **Modales suaves** — con backdrop blur

## 📁 Estructura

\`\`\`
frontend/src/
├── layouts/
│   └── Layout.astro        ← Layout base + sistema de toasts
├── lib/
│   ├── api.js              ← Cliente API (JavaScript puro)
│   └── auth.js             ← Utilidades de auth (JavaScript puro)
├── pages/
│   ├── index.astro         ← Landing page con orbes animados
│   ├── login.astro         ← Login con panel decorativo
│   ├── register.astro      ← Registro + indicador de fortaleza de contraseña
│   ├── dashboard.astro     ← Dashboard con estadísticas animadas
│   ├── products.astro      ← Catálogo con filtros + CRUD admin
│   ├── profile.astro       ← Perfil con edición inline + cambio de contraseña
│   └── users.astro         ← Gestión de usuarios (solo admin)
└── styles/
    └── global.css          ← Sistema de diseño completo
\`\`\`

## 🚀 Inicio Rápido

\`\`\`bash
cd frontend
npm install
cp .env.example .env
# Editar .env con tu URL del backend
npm run dev
\`\`\`

Frontend disponible en: **http://localhost:4321**

## 🎨 Páginas y Funcionalidades

| Página | URL | Requiere Auth |
|--------|-----|---------------|
| Landing | / | No |
| Login | /login | No |
| Registro | /register | No |
| Dashboard | /dashboard | ✓ User |
| Productos | /products | Público (CRUD solo Admin) |
| Perfil | /profile | ✓ User |
| Usuarios | /users | ✓ Admin |

## 🔧 Sin TypeScript

Todo el código está en JavaScript puro (.js). No se requiere conocimiento de TypeScript.
