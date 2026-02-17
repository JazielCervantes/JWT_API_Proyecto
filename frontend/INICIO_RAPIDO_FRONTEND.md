# 🚀 Frontend - Inicio Rápido

## ✅ Problema Resuelto: Error 404

El error 404 ocurría porque las páginas `.astro` no estaban creadas. **Ahora ya están incluidas** en el proyecto.

---

## 📋 Páginas Incluidas

### ✅ Páginas Principales (Ya Creadas)

- **`/`** - Landing page con hero y features
- **`/login`** - Inicio de sesión
- **`/register`** - Registro de usuarios
- **`/dashboard`** - Panel del usuario autenticado
- **`/products`** - Catálogo de productos con búsqueda
- **`/profile`** - Perfil del usuario

### 📂 Archivos Creados

```
frontend/src/
├── layouts/
│   └── Layout.astro          ✅ Layout principal
├── lib/
│   ├── api.ts               ✅ Cliente API
│   └── auth.ts              ✅ Gestión auth
├── pages/
│   ├── index.astro          ✅ Landing page
│   ├── login.astro          ✅ Login
│   ├── register.astro       ✅ Registro
│   ├── dashboard.astro      ✅ Dashboard
│   ├── products.astro       ✅ Productos
│   └── profile.astro        ✅ Perfil
└── styles/
    └── global.css           ✅ Estilos globales
```

---

## 🚀 Inicio Rápido (3 Pasos)

### 1. Instalar Dependencias

```bash
cd frontend
npm install
```

### 2. Configurar Variables de Entorno

```bash
cp .env.example .env
```

Edita `.env`:
```env
PUBLIC_API_URL=http://localhost:8000
```

### 3. Iniciar Servidor

```bash
npm run dev
```

✅ **Frontend corriendo en**: http://localhost:4321

---

## 🎯 Probar la Aplicación

### 1. Landing Page
Abre: http://localhost:4321

Deberías ver:
- Hero con título "API REST Profesional"
- Features (Autenticación, Roles, CRUD)
- Call to action

### 2. Registro
1. Click en "Comenzar ahora" o ve a `/register`
2. Completa el formulario
3. Click en "Crear Cuenta"
4. Serás redirigido al login

### 3. Login
1. Ve a `/login` o usa las credenciales demo:
   - Usuario: `admin`
   - Contraseña: `admin123`
2. Click en "Iniciar Sesión"
3. Serás redirigido al dashboard

### 4. Dashboard
Verás:
- Estadísticas (total productos, tu rol)
- Productos recientes
- Acciones rápidas

### 5. Productos
Ve a `/products`:
- Ver catálogo completo
- Buscar productos
- Paginación

### 6. Perfil
Ve a `/profile`:
- Tu información personal
- Rol y fecha de registro

---

## ⚠️ Requisitos Previos

### El Backend Debe Estar Corriendo

Asegúrate de que el backend esté activo:

```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
uvicorn app.main:app --reload
```

Verifica: http://localhost:8000/docs

---

## 🔧 Comandos Disponibles

```bash
# Desarrollo
npm run dev           # Inicia servidor de desarrollo

# Build
npm run build         # Compila para producción

# Preview
npm run preview       # Vista previa del build

# Type checking
npm run astro check   # Verifica tipos TypeScript
```

---

## 🚨 Troubleshooting

### Error: "Cannot find module 'astro'"

**Solución:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Error: "Failed to fetch" en login

**Causa:** Backend no está corriendo o URL incorrecta

**Solución:**
1. Verifica que el backend esté en http://localhost:8000
2. Verifica `.env`: `PUBLIC_API_URL=http://localhost:8000`
3. Reinicia el frontend

### Error de CORS

**Causa:** Backend no permite requests desde localhost:4321

**Solución:**
En `backend/.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4321
```

Reinicia el backend.

### Página en blanco

**Solución:**
1. Abre DevTools (F12) y revisa la consola
2. Verifica que el archivo `.astro` exista en `src/pages/`
3. Reinicia el servidor: Ctrl+C y `npm run dev`

---

## 🎨 Personalización

### Cambiar Colores

Edita `frontend/tailwind.config.mjs`:

```javascript
colors: {
  apple: {
    blue: '#0071E3',  // Cambia a tu color
    green: '#34C759',
    red: '#FF3B30',
    // ...
  }
}
```

### Cambiar Textos

Edita directamente los archivos `.astro` en `src/pages/`

### Agregar Logo

1. Agrega tu logo en `public/logo.svg`
2. Úsalo en las páginas:
```html
<img src="/logo.svg" alt="Logo" class="w-8 h-8" />
```

---

## 📱 Vista Mobile

El diseño es completamente responsive. Prueba:

1. Abre DevTools (F12)
2. Click en el ícono de móvil
3. Selecciona un dispositivo
4. Navega por la app

---

## 🎯 Próximos Pasos

1. ✅ Frontend funcionando localmente
2. ✅ Prueba todas las páginas
3. ✅ Registra un usuario
4. ✅ Explora el dashboard
5. 📝 Personaliza el diseño
6. 🚀 Despliega en Vercel (ver `docs/DESPLIEGUE_VERCEL.md`)

---

## 📚 Estructura de Componentes

Si quieres crear componentes Vue reutilizables (opcional):

```bash
# Crear componente
mkdir -p src/components/UI
touch src/components/UI/Button.vue
```

Ver código de ejemplo en: `frontend/GUIA_COMPLETA_FRONTEND.md`

---

## ✅ Checklist

- [ ] Node.js instalado
- [ ] `npm install` ejecutado
- [ ] `.env` configurado
- [ ] Backend corriendo en :8000
- [ ] Frontend corriendo en :4321
- [ ] Puedes ver la landing page
- [ ] Puedes hacer login
- [ ] Dashboard se carga correctamente

---

## 🎉 ¡Listo!

Tu frontend ya está funcionando con:
- ✅ Diseño minimalista estilo Apple
- ✅ 6 páginas completas
- ✅ Autenticación JWT
- ✅ Cliente API completo
- ✅ Responsive design
- ✅ Animaciones suaves

**¿Problemas?** Revisa la consola del navegador (F12) para ver errores específicos.

---

**Siguiente paso**: Personaliza y despliega en Vercel (gratis)
