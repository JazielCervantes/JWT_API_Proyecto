# 🎨 Guía Completa del Frontend - Código de Componentes y Páginas

Esta guía contiene todo el código necesario para completar el frontend.

## 📁 Estructura Completa

```
frontend/src/
├── components/
│   └── UI/
│       ├── Button.vue
│       ├── Card.vue
│       ├── Input.vue
│       ├── Modal.vue
│       └── Navbar.vue
├── layouts/
│   └── Layout.astro
├── lib/
│   ├── api.ts
│   └── auth.ts
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

---

## 🧩 Componentes Vue (src/components/UI/)

### Button.vue

```vue
<template>
  <button 
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="animate-spin mr-2">⏳</span>
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
}>();

const buttonClasses = computed(() => {
  const base = 'inline-flex items-center justify-center font-medium rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'bg-apple-blue text-white hover:bg-blue-600 focus:ring-apple-blue',
    secondary: 'bg-apple-gray-100 text-apple-gray-900 hover:bg-apple-gray-200',
    danger: 'bg-apple-red text-white hover:bg-red-600 focus:ring-apple-red'
  };
  
  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  };
  
  return [
    base,
    variants[props.variant || 'primary'],
    sizes[props.size || 'md'],
    props.fullWidth && 'w-full'
  ].filter(Boolean).join(' ');
});
</script>
```

### Card.vue

```vue
<template>
  <div :class="cardClasses">
    <div v-if="$slots.header" class="mb-4 pb-4 border-b border-apple-gray-200">
      <slot name="header" />
    </div>
    <slot />
    <div v-if="$slots.footer" class="mt-4 pt-4 border-t border-apple-gray-200">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  hover?: boolean;
  padding?: 'sm' | 'md' | 'lg';
}>();

const cardClasses = computed(() => {
  const base = 'bg-white rounded-2xl shadow-apple transition-all';
  const paddings = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  };
  
  return [
    base,
    paddings[props.padding || 'md'],
    props.hover && 'hover:shadow-apple-lg cursor-pointer'
  ].filter(Boolean).join(' ');
});
</script>
```

### Input.vue

```vue
<template>
  <div class="space-y-2">
    <label v-if="label" :for="id" class="block text-sm font-medium text-apple-gray-700">
      {{ label }}
      <span v-if="required" class="text-apple-red">*</span>
    </label>
    <div class="relative">
      <input
        :id="id"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        class="w-full px-4 py-3 rounded-xl border border-apple-gray-300 focus:border-apple-blue focus:ring-2 focus:ring-apple-blue focus:ring-opacity-20 transition-all outline-none disabled:bg-apple-gray-50 disabled:cursor-not-allowed"
      />
    </div>
    <p v-if="error" class="text-sm text-apple-red">
      {{ error }}
    </p>
    <p v-else-if="hint" class="text-sm text-apple-gray-500">
      {{ hint }}
    </p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  id?: string;
  label?: string;
  type?: string;
  modelValue?: string | number;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  error?: string;
  hint?: string;
}>();

defineEmits<{
  'update:modelValue': [value: string];
}>();
</script>
```

### Modal.vue

```vue
<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="fixed inset-0 z-50 overflow-y-auto">
        <!-- Backdrop -->
        <div 
          class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
          @click="close"
        ></div>
        
        <!-- Modal -->
        <div class="flex min-h-screen items-center justify-center p-4">
          <div 
            class="relative bg-white rounded-3xl shadow-apple-lg max-w-lg w-full p-6 animate-slide-up"
            @click.stop
          >
            <!-- Header -->
            <div v-if="$slots.header || title" class="mb-4">
              <slot name="header">
                <h3 class="text-2xl font-semibold text-apple-gray-900">{{ title }}</h3>
              </slot>
            </div>
            
            <!-- Body -->
            <div class="mb-6">
              <slot />
            </div>
            
            <!-- Footer -->
            <div v-if="$slots.footer" class="flex justify-end space-x-3">
              <slot name="footer" />
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: boolean;
  title?: string;
}>();

const emit = defineEmits<{
  'update:modelValue': [value: boolean];
}>();

function close() {
  emit('update:modelValue', false);
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
```

### Navbar.vue

```vue
<template>
  <nav class="bg-white border-b border-apple-gray-200 sticky top-0 z-40 backdrop-blur-lg bg-opacity-90">
    <div class="container-apple">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <a href="/" class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-apple-blue rounded-lg"></div>
          <span class="text-xl font-semibold text-apple-gray-900">JWT API</span>
        </a>
        
        <!-- Navigation -->
        <div class="hidden md:flex items-center space-x-1">
          <a 
            v-for="item in navItems" 
            :key="item.href"
            :href="item.href"
            class="px-4 py-2 rounded-lg text-apple-gray-700 hover:bg-apple-gray-100 transition-colors"
          >
            {{ item.label }}
          </a>
        </div>
        
        <!-- User menu -->
        <div v-if="user" class="flex items-center space-x-4">
          <span class="text-sm text-apple-gray-600">{{ user.username }}</span>
          <button 
            @click="handleLogout"
            class="text-sm text-apple-red hover:text-red-600"
          >
            Cerrar sesión
          </button>
        </div>
        <div v-else class="flex items-center space-x-2">
          <a href="/login" class="btn-secondary">Iniciar sesión</a>
          <a href="/register" class="btn-primary">Registrarse</a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getUser, isAdmin } from '@lib/auth';
import api from '@lib/api';

const user = ref<any>(null);

const navItems = ref([
  { label: 'Dashboard', href: '/dashboard' },
  { label: 'Productos', href: '/products' },
]);

onMounted(() => {
  user.value = getUser();
  if (user.value && isAdmin()) {
    navItems.value.push({ label: 'Usuarios', href: '/users' });
  }
});

async function handleLogout() {
  await api.logout();
}
</script>
```

---

## 📄 Páginas Astro (src/pages/)

### index.astro (Landing Page)

```astro
---
import Layout from '../layouts/Layout.astro';
---

<Layout title="JWT API App - Home">
  <div class="min-h-screen bg-gradient-to-b from-white to-apple-gray-50">
    <!-- Hero Section -->
    <section class="container-apple py-20 md:py-32">
      <div class="text-center space-y-8 animate-fade-in">
        <h1 class="text-6xl md:text-7xl font-bold text-apple-gray-900">
          API REST Profesional
        </h1>
        <p class="text-xl md:text-2xl text-apple-gray-600 max-w-3xl mx-auto">
          Sistema completo de autenticación con JWT, roles de usuario y gestión de productos
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center pt-8">
          <a href="/register" class="btn-primary text-lg">
            Comenzar ahora
          </a>
          <a href="/products" class="btn-secondary text-lg">
            Ver productos
          </a>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="container-apple py-20">
      <div class="grid md:grid-cols-3 gap-8">
        <div class="card text-center space-y-4">
          <div class="text-4xl">🔐</div>
          <h3 class="text-xl font-semibold">Autenticación Segura</h3>
          <p class="text-apple-gray-600">JWT con refresh tokens y hash bcrypt</p>
        </div>
        <div class="card text-center space-y-4">
          <div class="text-4xl">👥</div>
          <h3 class="text-xl font-semibold">Sistema de Roles</h3>
          <p class="text-apple-gray-600">Control de acceso granular por roles</p>
        </div>
        <div class="card text-center space-y-4">
          <div class="text-4xl">📦</div>
          <h3 class="text-xl font-semibold">CRUD Completo</h3>
          <p class="text-apple-gray-600">Gestión completa de productos y usuarios</p>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="container-apple py-20 text-center">
      <div class="bg-apple-blue text-white rounded-3xl p-12 space-y-6">
        <h2 class="text-4xl font-bold">¿Listo para comenzar?</h2>
        <p class="text-xl opacity-90">Crea tu cuenta gratis en segundos</p>
        <a href="/register" class="inline-block bg-white text-apple-blue px-8 py-4 rounded-xl font-semibold hover:bg-gray-100 transition-colors">
          Registrarse gratis
        </a>
      </div>
    </section>
  </div>
</Layout>
```

### login.astro

```astro
---
import Layout from '../layouts/Layout.astro';
---

<Layout title="Iniciar Sesión">
  <div class="min-h-screen flex items-center justify-center bg-apple-gray-50 py-12 px-4">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-apple-gray-900">Iniciar Sesión</h2>
        <p class="mt-2 text-apple-gray-600">Ingresa a tu cuenta</p>
      </div>
      
      <div class="card">
        <form id="loginForm" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-apple-gray-700 mb-2">
              Usuario o Email
            </label>
            <input 
              type="text" 
              name="username" 
              required
              class="input"
              placeholder="usuario123"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-apple-gray-700 mb-2">
              Contraseña
            </label>
            <input 
              type="password" 
              name="password" 
              required
              class="input"
              placeholder="••••••••"
            />
          </div>
          
          <div id="error" class="hidden text-sm text-apple-red"></div>
          
          <button type="submit" class="btn-primary w-full">
            Iniciar Sesión
          </button>
        </form>
        
        <p class="mt-6 text-center text-sm text-apple-gray-600">
          ¿No tienes cuenta? 
          <a href="/register" class="text-apple-blue hover:underline">Regístrate aquí</a>
        </p>
      </div>
    </div>
  </div>
</Layout>

<script>
  import api from '../lib/api';
  import { saveUser } from '../lib/auth';
  
  const form = document.getElementById('loginForm') as HTMLFormElement;
  const errorDiv = document.getElementById('error') as HTMLDivElement;
  
  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorDiv.classList.add('hidden');
    
    const formData = new FormData(form);
    const username = formData.get('username') as string;
    const password = formData.get('password') as string;
    
    try {
      await api.login(username, password);
      const user = await api.getCurrentUser();
      saveUser(user);
      window.location.href = '/dashboard';
    } catch (error: any) {
      errorDiv.textContent = error.message || 'Error al iniciar sesión';
      errorDiv.classList.remove('hidden');
    }
  });
</script>
```

### register.astro

```astro
---
import Layout from '../layouts/Layout.astro';
---

<Layout title="Registro">
  <div class="min-h-screen flex items-center justify-center bg-apple-gray-50 py-12 px-4">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-apple-gray-900">Crear Cuenta</h2>
        <p class="mt-2 text-apple-gray-600">Regístrate gratis</p>
      </div>
      
      <div class="card">
        <form id="registerForm" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-apple-gray-700 mb-2">
              Nombre Completo
            </label>
            <input 
              type="text" 
              name="full_name" 
              required
              class="input"
              placeholder="Juan Pérez"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-apple-gray-700 mb-2">
              Email
            </label>
            <input 
              type="email" 
              name="email" 
              required
              class="input"
              placeholder="juan@ejemplo.com"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-apple-gray-700 mb-2">
              Usuario
            </label>
            <input 
              type="text" 
              name="username" 
              required
              class="input"
              placeholder="juanperez"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-apple-gray-700 mb-2">
              Contraseña
            </label>
            <input 
              type="password" 
              name="password" 
              required
              minlength="6"
              class="input"
              placeholder="Mínimo 6 caracteres"
            />
          </div>
          
          <div id="error" class="hidden text-sm text-apple-red"></div>
          
          <button type="submit" class="btn-primary w-full">
            Crear Cuenta
          </button>
        </form>
        
        <p class="mt-6 text-center text-sm text-apple-gray-600">
          ¿Ya tienes cuenta? 
          <a href="/login" class="text-apple-blue hover:underline">Inicia sesión aquí</a>
        </p>
      </div>
    </div>
  </div>
</Layout>

<script>
  import api from '../lib/api';
  
  const form = document.getElementById('registerForm') as HTMLFormElement;
  const errorDiv = document.getElementById('error') as HTMLDivElement;
  
  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorDiv.classList.add('hidden');
    
    const formData = new FormData(form);
    const userData = {
      full_name: formData.get('full_name') as string,
      email: formData.get('email') as string,
      username: formData.get('username') as string,
      password: formData.get('password') as string,
    };
    
    try {
      await api.register(userData);
      window.location.href = '/login?registered=true';
    } catch (error: any) {
      errorDiv.textContent = error.message || 'Error al crear la cuenta';
      errorDiv.classList.remove('hidden');
    }
  });
</script>
```

### dashboard.astro

```astro
---
import Layout from '../layouts/Layout.astro';
---

<Layout title="Dashboard">
  <div id="navbar-container"></div>
  
  <div class="min-h-screen bg-apple-gray-50 py-8">
    <div class="container-apple">
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-apple-gray-900">Dashboard</h1>
        <p class="mt-2 text-apple-gray-600">Bienvenido de vuelta</p>
      </div>
      
      <div id="loading" class="text-center py-12">
        <div class="animate-spin text-4xl">⏳</div>
        <p class="mt-4 text-apple-gray-600">Cargando...</p>
      </div>
      
      <div id="content" class="hidden space-y-8">
        <!-- Stats -->
        <div class="grid md:grid-cols-3 gap-6">
          <div class="card">
            <h3 class="text-apple-gray-600 text-sm font-medium">Total Productos</h3>
            <p id="totalProducts" class="text-3xl font-bold text-apple-gray-900 mt-2">0</p>
          </div>
          <div class="card">
            <h3 class="text-apple-gray-600 text-sm font-medium">Tu Rol</h3>
            <p id="userRole" class="text-3xl font-bold text-apple-blue mt-2">-</p>
          </div>
          <div class="card">
            <h3 class="text-apple-gray-600 text-sm font-medium">Estado</h3>
            <p class="text-3xl font-bold text-apple-green mt-2">✓ Activo</p>
          </div>
        </div>
        
        <!-- Actions -->
        <div class="card">
          <h2 class="text-2xl font-semibold mb-4">Acciones Rápidas</h2>
          <div class="grid sm:grid-cols-2 gap-4">
            <a href="/products" class="btn-primary text-center">Ver Productos</a>
            <a href="/profile" class="btn-secondary text-center">Mi Perfil</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</Layout>

<script>
  import { requireAuth, getUser } from '../lib/auth';
  import api from '../lib/api';
  
  requireAuth();
  
  const user = getUser();
  document.getElementById('userRole')!.textContent = user?.role || '-';
  
  // Load stats
  api.getProducts({ limit: 1 }).then(data => {
    document.getElementById('totalProducts')!.textContent = data.total.toString();
    document.getElementById('loading')!.classList.add('hidden');
    document.getElementById('content')!.classList.remove('hidden');
  }).catch(error => {
    console.error('Error loading dashboard:', error);
  });
</script>
```

---

## 📋 Instrucciones Finales

### 1. Instalar dependencias

```bash
cd frontend
npm install
```

### 2. Configurar .env

```bash
cp .env.example .env
```

Edita `.env`:
```env
PUBLIC_API_URL=http://localhost:8000
```

### 3. Iniciar frontend

```bash
npm run dev
```

### 4. Páginas adicionales

Para completar el frontend, crea estas páginas adicionales siguiendo el mismo patrón:

- **products.astro**: Lista de productos con filtros
- **users.astro**: Gestión de usuarios (admin only)
- **profile.astro**: Perfil del usuario

### 5. Build para producción

```bash
npm run build
npm run preview
```

El build estará en `dist/`

---

## 🎨 Personalización

- **Colores**: Modifica `tailwind.config.mjs`
- **Logo**: Agrega tu logo en `public/`
- **Textos**: Edita directamente en las páginas `.astro`
- **Componentes**: Crea nuevos en `src/components/`

---

**¡Tu frontend estilo Apple está listo!** 🎉
