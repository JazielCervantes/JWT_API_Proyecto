# 🚀 Guía Maestra: De Cero a Producción

## 📋 Índice

Esta guía te llevará desde la instalación hasta tener tu app completa en producción.

1. [Configuración Local](#1-configuración-local)
2. [Frontend con Astro](#2-frontend-con-astro)
3. [Subir a GitHub](#3-subir-a-github)
4. [Desplegar Backend](#4-desplegar-backend)
5. [Desplegar Frontend](#5-desplegar-frontend)
6. [Configuración Final](#6-configuración-final)
7. [Verificación](#7-verificación)

---

## 1. Configuración Local

### Backend (FastAPI)

```bash
# 1. Instalar MySQL
# Ver INICIO_RAPIDO.md

# 2. Crear base de datos
mysql -u root -p -e "CREATE DATABASE jwt_api_db;"

# 3. Configurar backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Editar .env con tus credenciales

# 5. Crear tablas
python -m app.database

# 6. Iniciar backend
uvicorn app.main:app --reload
```

✅ Backend corriendo en: http://localhost:8000

### Frontend (Astro)

```bash
# 1. Instalar dependencias
cd frontend
npm install

# 2. Configurar .env
cp .env.example .env
# Editar .env:
# PUBLIC_API_URL=http://localhost:8000

# 3. Iniciar frontend
npm run dev
```

✅ Frontend corriendo en: http://localhost:4321

---

## 2. Frontend con Astro

El proyecto incluye el código base. Para completar:

### Crear Componentes Faltantes

Sigue la guía en `frontend/GUIA_COMPLETA_FRONTEND.md` para crear:

1. **Componentes UI** (Button, Card, Input, Modal, Navbar)
2. **Páginas** (index, login, register, dashboard, products, users, profile)

### Estructura Completa

```
frontend/
├── src/
│   ├── components/
│   │   └── UI/
│   │       ├── Button.vue
│   │       ├── Card.vue
│   │       ├── Input.vue
│   │       ├── Modal.vue
│   │       └── Navbar.vue
│   ├── layouts/
│   │   └── Layout.astro
│   ├── lib/
│   │   ├── api.ts           ✅ Ya creado
│   │   └── auth.ts          ✅ Ya creado
│   ├── pages/
│   │   ├── index.astro      ⚠️ Crear con código de la guía
│   │   ├── login.astro      ⚠️ Crear con código de la guía
│   │   ├── register.astro   ⚠️ Crear con código de la guía
│   │   ├── dashboard.astro  ⚠️ Crear con código de la guía
│   │   ├── products.astro   ⚠️ Crear (similar a dashboard)
│   │   ├── users.astro      ⚠️ Crear (solo admin)
│   │   └── profile.astro    ⚠️ Crear
│   └── styles/
│       └── global.css       ✅ Ya creado
├── package.json             ✅ Ya creado
├── astro.config.mjs        ✅ Ya creado
└── tailwind.config.mjs     ✅ Ya creado
```

### Verificar que Funciona

```bash
cd frontend
npm run dev
```

Prueba:
1. Landing page (`/`)
2. Registro (`/register`)
3. Login (`/login`)
4. Dashboard (`/dashboard`)

---

## 3. Subir a GitHub

### Preparar el Proyecto

```bash
# En la raíz del proyecto
git init
git add .
git commit -m "Initial commit: API REST con JWT + Frontend Astro"
```

### Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre: `jwt-api-project`
3. **NO** marques "Initialize with README"
4. Click **Create repository**

### Conectar y Subir

```bash
# Reemplaza TU_USUARIO con tu usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/jwt-api-project.git
git branch -M main
git push -u origin main
```

✅ Código en GitHub: `https://github.com/TU_USUARIO/jwt-api-project`

**Guía completa**: `docs/GITHUB_SETUP.md`

---

## 4. Desplegar Backend

### Opción A: Railway (Recomendado)

1. Ve a https://railway.app
2. Login con GitHub
3. **New Project** → **Deploy from GitHub repo**
4. Selecciona `jwt-api-project`
5. Configura:
   - Root Directory: `backend/`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

6. **Add MySQL Database**:
   - Click **+ New** → **Database** → **MySQL**

7. **Variables de Entorno**:
   ```env
   DATABASE_URL=${{MySQL.DATABASE_URL}}
   SECRET_KEY=[genera con: python -c "import secrets; print(secrets.token_hex(32))"]
   DEBUG=False
   ALLOWED_ORIGINS=https://tu-proyecto.vercel.app,https://*.vercel.app
   ADMIN_PASSWORD=password_seguro_aqui
   ```

8. **Deploy** y espera 2-3 minutos

9. **Generate Domain** en Settings → Networking

✅ Backend en: `https://tu-backend.railway.app`

**Guía completa**: `docs/DESPLIEGUE_RAILWAY.md`

### Opción B: Render

Similar proceso, ver guía en `DESPLIEGUE_RAILWAY.md`.

---

## 5. Desplegar Frontend

### Vercel (Recomendado)

1. Ve a https://vercel.com
2. Login con GitHub
3. **Add New...** → **Project**
4. Selecciona `jwt-api-project`
5. Configura:
   - Framework: **Astro**
   - Root Directory: `frontend/`
   - Build Command: `npm run build`
   - Output Directory: `dist`

6. **Environment Variables**:
   ```env
   PUBLIC_API_URL=https://tu-backend.railway.app
   ```

7. **Deploy** y espera 1-2 minutos

✅ Frontend en: `https://tu-proyecto.vercel.app`

**Guía completa**: `docs/DESPLIEGUE_VERCEL.md`

---

## 6. Configuración Final

### Actualizar CORS en el Backend

1. Ve a Railway
2. **Variables** → Edita `ALLOWED_ORIGINS`
3. Agrega tu URL de Vercel:
   ```env
   ALLOWED_ORIGINS=https://tu-proyecto.vercel.app,https://*.vercel.app
   ```
4. **Redeploy**

### Verificar Variables

#### Backend (Railway)
- ✅ `DATABASE_URL` configurado
- ✅ `SECRET_KEY` único y seguro
- ✅ `ALLOWED_ORIGINS` incluye URL de Vercel
- ✅ `ADMIN_PASSWORD` cambiado
- ✅ `DEBUG=False`

#### Frontend (Vercel)
- ✅ `PUBLIC_API_URL` apunta a Railway

---

## 7. Verificación

### Probar el Backend

```bash
# API Docs
https://tu-backend.railway.app/docs

# Health Check
curl https://tu-backend.railway.app/health

# Login Test (en Swagger)
POST /api/auth/login
{
  "username": "admin",
  "password": "tu_password"
}
```

### Probar el Frontend

1. Abre `https://tu-proyecto.vercel.app`
2. Click en "Registrarse"
3. Crea una cuenta
4. Inicia sesión
5. Explora el dashboard
6. Ver productos
7. Si eres admin, gestionar usuarios

### Probar Integración

1. Registro → Debe crear usuario en Railway
2. Login → Debe retornar tokens
3. Dashboard → Debe mostrar datos del usuario
4. Productos → Debe cargar desde la API
5. Logout → Debe limpiar sesión

---

## 🎯 Checklist Final

### Seguridad
- [ ] `.env` en `.gitignore`
- [ ] SECRET_KEY única en producción
- [ ] ADMIN_PASSWORD cambiado
- [ ] DEBUG=False en producción
- [ ] HTTPS habilitado (automático)
- [ ] CORS configurado correctamente

### Funcionalidad
- [ ] Registro funciona
- [ ] Login funciona
- [ ] Tokens se refrescan
- [ ] Dashboard carga
- [ ] Productos se muestran
- [ ] Admin puede gestionar usuarios

### Despliegue
- [ ] Backend en Railway
- [ ] Frontend en Vercel
- [ ] Base de datos MySQL creada
- [ ] URLs conectadas correctamente
- [ ] Deploy automático desde GitHub

---

## 📊 URLs Finales

Una vez completado, tendrás:

- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend API**: `https://tu-backend.railway.app`
- **API Docs**: `https://tu-backend.railway.app/docs`
- **GitHub**: `https://github.com/TU_USUARIO/jwt-api-project`

---

## 🎨 Personalización

### Cambiar Colores

Edita `frontend/tailwind.config.mjs`:
```javascript
colors: {
  apple: {
    blue: '#0071E3',  // Cambia esto
    // ...
  }
}
```

### Agregar Logo

1. Agrega `logo.svg` en `frontend/public/`
2. Usa en componentes:
   ```html
   <img src="/logo.svg" alt="Logo" />
   ```

### Cambiar Textos

Edita directamente las páginas `.astro` en `frontend/src/pages/`

---

## 🚨 Troubleshooting

### Error de CORS

**Síntoma**: Frontend no puede llamar al backend

**Solución**:
1. Verifica `ALLOWED_ORIGINS` en Railway
2. Debe incluir URL exacta de Vercel
3. Redeploy backend

### Build Failed en Vercel

**Síntoma**: Deploy falla en Vercel

**Solución**:
1. Verifica que `npm run build` funcione localmente
2. Revisa logs en Vercel
3. Asegúrate de que Root Directory sea `frontend/`

### Base de Datos Vacía

**Síntoma**: No hay tablas en MySQL

**Solución**:
1. Verifica logs en Railway
2. El backend debe crear tablas al iniciar
3. Si no, conéctate a MySQL y ejecuta:
   ```sql
   CREATE TABLE users (...);
   CREATE TABLE products (...);
   ```

---

## 💰 Costos

### Totalmente Gratis

- ✅ **Railway**: $5 gratis/mes (suficiente para proyectos pequeños)
- ✅ **Vercel**: Gratis ilimitado para proyectos personales
- ✅ **GitHub**: Gratis para repos públicos

**Total: $0/mes** para proyectos personales y portafolios

### Si Necesitas Más

- **Railway Developer**: $10/mes
- **Vercel Pro**: $20/mes

---

## 🎓 Aprendizaje

### ¿Qué has construido?

1. ✅ **API REST profesional** con FastAPI
2. ✅ **Frontend moderno** con Astro + Vue.js
3. ✅ **Autenticación JWT** completa
4. ✅ **Sistema de roles** funcional
5. ✅ **Base de datos** en la nube
6. ✅ **CI/CD** automático
7. ✅ **App en producción** accesible globalmente

### Skills Desarrollados

- Backend con Python/FastAPI
- Frontend con Astro/Vue.js
- Autenticación y seguridad
- Git y GitHub
- Deploy y DevOps
- MySQL y ORMs
- APIs RESTful

---

## 📚 Recursos Adicionales

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Astro Docs](https://docs.astro.build/)
- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)

---

## 🎯 Próximos Pasos

1. **Personaliza** el diseño
2. **Agrega features**: 
   - Recuperación de contraseña
   - Verificación de email
   - Upload de imágenes
   - Notificaciones
3. **Mejora el SEO**
4. **Agrega analytics**
5. **Comparte** en redes sociales
6. **Úsalo en tu portafolio**

---

## ⭐ Comparte tu Proyecto

Una vez tengas todo funcionando:

1. Agrega capturas de pantalla al README
2. Agrega badges:
   ```markdown
   ![GitHub stars](https://img.shields.io/github/stars/TU_USUARIO/jwt-api-project)
   ![License](https://img.shields.io/github/license/TU_USUARIO/jwt-api-project)
   ```
3. Tweet sobre tu proyecto
4. Agrégalo a tu LinkedIn
5. Muéstralo en entrevistas

---

**¡Felicidades! Tienes una aplicación full-stack en producción** 🎉

**De cero a producción**: ✅ Completado
