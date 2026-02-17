# 🎨 Frontend con Astro - Guía Completa

## 📋 Descripción

Frontend minimalista estilo Apple con Astro + Vue.js que consume la API REST.

## ✨ Características

- ✅ Diseño minimalista estilo Apple
- ✅ Autenticación completa (login/registro)
- ✅ Dashboard de usuario
- ✅ CRUD de productos con filtros
- ✅ Panel de administración
- ✅ Gestión de perfil
- ✅ Responsive design
- ✅ Animaciones suaves
- ✅ Manejo de tokens JWT

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
cd frontend
npm install
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env`:
```env
PUBLIC_API_URL=http://localhost:8000
```

### 3. Iniciar servidor de desarrollo

```bash
npm run dev
```

El frontend estará disponible en: http://localhost:4321

## 📦 Tecnologías Utilizadas

- **Astro 4.0** - Framework estático
- **Vue.js 3** - Componentes interactivos
- **TailwindCSS** - Estilos utility-first
- **TypeScript** - Tipado estático
- **Lucide Icons** - Iconos minimalistas

## 📁 Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/          # Componentes Vue.js
│   │   ├── Auth/           # Login, Register
│   │   ├── Dashboard/      # Dashboard principal
│   │   ├── Products/       # Lista, crear, editar productos
│   │   ├── Users/          # Gestión de usuarios (admin)
│   │   └── UI/             # Componentes reutilizables
│   │
│   ├── layouts/            # Layouts de Astro
│   │   └── Layout.astro    # Layout principal
│   │
│   ├── pages/              # Rutas de la aplicación
│   │   ├── index.astro     # Landing page
│   │   ├── login.astro     # Login
│   │   ├── register.astro  # Registro
│   │   ├── dashboard.astro # Dashboard
│   │   └── products.astro  # Productos
│   │
│   ├── lib/                # Utilidades
│   │   ├── api.ts          # Cliente API
│   │   └── auth.ts         # Gestión de autenticación
│   │
│   └── styles/             # Estilos globales
│       └── global.css
│
├── public/                 # Archivos estáticos
├── astro.config.mjs       # Configuración Astro
├── tailwind.config.mjs    # Configuración Tailwind
└── package.json
```

## 🎨 Diseño Estilo Apple

### Principios de Diseño

1. **Minimalismo**: Espacios en blanco generosos
2. **Tipografía**: Sistema de fuentes clara y legible
3. **Colores**: Paleta neutral con acentos sutiles
4. **Animaciones**: Transiciones suaves y elegantes
5. **Responsive**: Mobile-first approach

### Paleta de Colores

```css
/* Tonos neutros */
background: #FFFFFF
surface: #F5F5F7
text-primary: #1D1D1F
text-secondary: #86868B

/* Acentos */
primary: #0071E3 (Azul Apple)
success: #34C759
error: #FF3B30
warning: #FF9500
```

## 🔐 Gestión de Autenticación

### Flujo de Autenticación

1. Usuario hace login → Recibe access_token y refresh_token
2. Tokens se guardan en localStorage
3. Cada request incluye el access_token en el header
4. Si expira, se refresca automáticamente
5. Rutas protegidas redirigen a login si no hay token

### Cliente API

```typescript
// src/lib/api.ts
const apiClient = {
  async request(endpoint, options) {
    const token = localStorage.getItem('access_token');
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` })
    };
    
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers
    });
    
    // Si token expiró, refrescar
    if (response.status === 401) {
      await refreshToken();
      // Reintentar request
    }
    
    return response.json();
  }
};
```

## 📱 Páginas Incluidas

### 1. Landing Page (/)
- Hero section
- Características
- Call to action
- Footer

### 2. Login (/login)
- Formulario de login
- Validación
- Manejo de errores
- Link a registro

### 3. Registro (/register)
- Formulario de registro
- Validación de campos
- Creación de cuenta

### 4. Dashboard (/dashboard)
- Vista general de estadísticas
- Productos recientes
- Acciones rápidas

### 5. Productos (/products)
- Lista con filtros
- Búsqueda
- Paginación
- Crear/Editar/Eliminar (admin)

### 6. Usuarios (/users) - Solo Admin
- Lista de usuarios
- Cambiar roles
- Activar/Desactivar

### 7. Perfil (/profile)
- Ver/Editar perfil
- Cambiar contraseña
- Cerrar sesión

## 🧩 Componentes Principales

### Button.vue
```vue
<template>
  <button 
    :class="buttonClasses"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>
```

### Card.vue
```vue
<template>
  <div class="bg-white rounded-2xl shadow-sm p-6">
    <slot />
  </div>
</template>
```

### Input.vue
```vue
<template>
  <div class="relative">
    <input 
      :type="type"
      :placeholder="placeholder"
      class="w-full px-4 py-3 rounded-xl border border-gray-200"
    />
  </div>
</template>
```

## 📊 Gestión de Estado

Se usa localStorage para persistencia:

```typescript
// Guardar tokens
localStorage.setItem('access_token', token);
localStorage.setItem('refresh_token', refreshToken);
localStorage.setItem('user', JSON.stringify(user));

// Leer datos
const user = JSON.parse(localStorage.getItem('user'));

// Limpiar (logout)
localStorage.clear();
```

## 🚀 Scripts Disponibles

```bash
# Desarrollo
npm run dev

# Build para producción
npm run build

# Preview del build
npm run preview

# Linting
npm run lint
```

## 🌐 Despliegue

Ver guías específicas:
- `DESPLIEGUE_VERCEL.md` - Desplegar en Vercel
- `DESPLIEGUE_NETLIFY.md` - Desplegar en Netlify
- `GITHUB_SETUP.md` - Subir a GitHub

## 🔒 Consideraciones de Seguridad

1. **Tokens en localStorage**: Apropiado para aplicaciones SPA
2. **HTTPS en producción**: Obligatorio
3. **CORS configurado**: Solo orígenes permitidos
4. **Validación client-side**: Mejorar UX, no reemplaza backend
5. **No incluir secrets**: Usar variables de entorno

## 📝 Notas

- El frontend es estático (Astro)
- Vue.js solo para componentes interactivos
- Optimizado para SEO
- Build rápido y ligero

## 🎯 Próximos Pasos

1. Personaliza los colores en `tailwind.config.mjs`
2. Agrega tu logo en `public/`
3. Modifica textos en las páginas
4. Despliega en Vercel o Netlify

---

**Versión**: 1.0.0  
**Framework**: Astro 4.0  
**Estilo**: Apple Minimalista
