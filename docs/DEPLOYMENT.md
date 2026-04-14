# 🚀 Despliegue a Producción

---

## ⚡ Quick Deploy (30 minutos)

**Total costo por mes: $0 (Vercel gratis + Railway $5 gratis)**

### Requisitos
- ✅ Código en GitHub
- ✅ Cuenta GitHub
- ✅ Backend funcionando localmente
- ✅ Frontend funcionando localmente

---

## 1️⃣ Backend - Railway

### Paso 1: Preparar Código

```bash
# Asegurar que el proyecto está en GitHub
cd jwt-api-project
git status
git push origin main
```

**Archivos necesarios en raíz:**
```
railway.json        ← Ya incluido
Procfile           ← Ya incluido
backend/
  requirements.txt ← Ya incluido
```

### Paso 2: Crear Cuenta Railroad

1. Ve a: https://railway.app
2. **Login** → **Login with GitHub**
3. Autoriza Railway

### Paso 3: Crear Proyecto

1. Click **New Project**
2. **Deploy from GitHub repo**
3. Busca y selecciona `jwt-api-project`
4. **Deploy Now**

### Paso 4: Configurar Base de Datos

1. En el proyecto, click **+ New**
2. Selecciona **Database** → **MySQL**
3. Railroad crea automáticamente una BD MySQL
4. Espera 2 minutos

### Paso 5: Configurar Variables de Entorno

En el dashboard de Railway:

**Click en tu servicio backend → Variables**

Agrega estas variables (copiar-pegar):

```env
DEBUG=False
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Generar SECRET_KEY:
# Ejecuta en terminal: python -c "import secrets; print(secrets.token_hex(32))"
# Copia el resultado y pégalo aquí:
SECRET_KEY=REEMPLAZAR_CON_RESULTADO_DEL_COMANDO

ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123           # CAMBIAR EN PRODUCCIÓN
ALLOWED_ORIGINS=*                 # Actualizar después con URL de Vercel

# Database - Railway la crea automático:
DATABASE_URL=${{MySQL.DATABASE_URL}}
```

### Paso 6: Verificar Deploy

1. En Railway, **View Logs**
2. Verifica que no haya errores
3. Busca: `✅ Aplicación iniciada correctamente`
4. Busca la URL del servidor (ej: `https://jwt-api-railway.up.railway.app`)

### Paso 7: Prueba Rápida

```bash
# Reemplaza con tu URL de Railway
curl https://jwt-api-railway.up.railway.app/docs

# Deberías ver la página de Swagger
```

✅ **Backend en**: https://tu-backend.railway.app

---

## 2️⃣ Frontend - Vercel

### Paso 1: Crear Cuenta Vercel

1. Ve a: https://vercel.com
2. **Sign Up** → **Continue with GitHub**
3. Autoriza Vercel

### Paso 2: Importar Proyecto

1. Click **Add New...** → **Project**
2. Busca y selecciona `jwt-api-project`
3. **Import**

### Paso 3: Configurar Proyecto

Vercel automáticamente detectará:
- Framework: **Astro**
- Root Directory: **frontend/** (asegúrate que esté correcto)

**Edita build settings:**
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

### Paso 4: Agregar Variable de Entorno

Click **Environment Variables** y agrega:

```
Name: PUBLIC_API_URL
Value: https://tu-backend.railway.app
```

(Reemplaza con tu URL real de Railway del paso anterior)

### Paso 5: Deploy

1. Click **Deploy**
2. Espera 2-3 minutos
3. Verás "✅ Deployment successful"

✅ **Frontend en**: https://tu-proyecto.vercel.app

---

## 3️⃣ Conectar Backend y Frontend

### Actualizar CORS en Railway

1. Ve a Railroad dashboard
2. Click en tu backend
3. **Variables** → Edita `ALLOWED_ORIGINS`
4. Cambia de:
   ```env
   ALLOWED_ORIGINS=*
   ```
   A:
   ```env
   ALLOWED_ORIGINS=https://tu-proyecto.vercel.app,https://*.vercel.app
   ```
5. **Save** (se redeploy automático)

### Verificar Integración

1. Abre https://tu-proyecto.vercel.app
2. Click **Iniciar Sesión**
3. Ingresa: `admin` / `admin123`
4. ¿Ves el dashboard? ✅ ¡Funcionó!
5. Intenta crear un producto
6. Intenta cambiar tu perfil

---

## ✅ Checklist de Despliegue

### Seguridad
- [ ] `SECRET_KEY` es único y seguro (32 caracteres)
- [ ] `ADMIN_PASSWORD` cambió de default
- [ ] `DEBUG=False` en producción
- [ ] HTTPS habilitado (automático en Railway + Vercel)
- [ ] `ALLOWED_ORIGINS` solo incluye tu dominio

### Funcionalidad
- [ ] Backend responde en su URL
- [ ] Frontend carga sin errores
- [ ] Swagger UI funciona
- [ ] Puedo hacer login
- [ ] Dashboard muestra datos
- [ ] Puedo crear/editar/eliminar productos
- [ ] Logout funciona

### Base de Datos
- [ ] MySQL funciona en Railway
- [ ] Tablas se crearon automáticamente
- [ ] Puedo insertar/actualizarregistros

---

## 🔐 Mejoras de Seguridad Recomendadas

### 1. Cambiar Admin Password

Cuando esté en producción:

```bash
# Genera password seguro:
openssl rand -base64 12

# Actualiza en Railway:
# Variables → ADMIN_PASSWORD → nuevo_password
```

### 2. Usar Dominios Personalizados

**Railway:**
1. Click tu proyecto
2. **Settings** → **Networking**
3. **Generate Domain** o agrega tu propio dominio

**Vercel:**
1. Click tu proyecto
2. **Settings** → **Domains**
3. Agrega tu dominio personalizado

### 3. Configurar Backups Automáticos

**Railway MySQL:**
1. Click servicio MySQL
2. **Settings** → **Backups**
3. Habilitar backups automáticos

### 4. Monitoreo

**Railway Logs:**
- En dashboard, **View Logs** para ver errores en tiempo real

**Vercel Analytics:**
- En dashboard, **Analytics** para ver performance

---

## 🚨 Troubleshooting del Despliegue

### ❌ Error: "Database connection failed"

**Causa:** DATABASE_URL no está correcta

**Solución:**
1. Ve a Railway
2. Click el servicio MySQL
3. Copia `DATABASE_URL` de **Variables expuestas**
4. Pégalo en el servicio backend

### ❌ Build failed en Vercel

**Causa:** Error en npm run build

**Solución:**
1. Verifica que `npm run build` funcione localmente
2. Revisa Vercel logs (clic en Build Log)
3. Asegúrate que Root Directory sea `frontend/`

### ❌ CORS errors en frontend

**Síntoma:** `Access to XMLHttpRequest blocked...`

**Solución:**
1. Ve a Railway
2. Verifica `ALLOWED_ORIGINS` incluye tu URL de Vercel
3. Redeploy backend (click **Redeploy**)

### ❌ Timeout al crear usuarios

**Causa:** Las tablas no se crearon

**Solución:**
1. Ve a Railway → Logs
2. Busca si hay errores de creación de tablas
3. Intenta redeploy

---

## 📊 URLs Finales

Una vez todo esté funcionando:

```
Frontend:        https://tu-proyecto.vercel.app
Backend API:     https://tu-backend.railway.app
API Docs:        https://tu-backend.railway.app/docs
GitHub Repo:     https://github.com/usuario/jwt-api-project
```

---

## 💰 Costos

### Totalmente Gratis

| Servicio | Costo | Límites |
|----------|-------|---------|
| **Vercel** | $0/mes | Ilimitado para proyectos personales |
| **Railway** | $5/mes gratis | Suficiente para proyectos pequeños |
| **GitHub** | $0/mes | Repos públicos ilimitados |
| **Total** | **$0/mes** | Perfect para portafolio |

---

## 🔄 Workflow Continuo

### Después de Desplegar

Cada vez que cambies código:

```bash
# 1. Haz cambios locales
# (edita archivos)

# 2. Commit y push
git add .
git commit -m "Descripción del cambio"
git push origin main

# 3. Deploy automático
# (Vercel y Railway redeploy automáticamente)

# 4. Verificar cambios
# (Abre https://tu-proyecto.vercel.app)
```

---

## 📚 Alternativas

Si quieres usar otras plataformas:

### Backend Alternativas a Railway
- **Render** (similar, $7/mes gratis)
- **Heroku** (pagado desde 2022, ~$7/mes)
- **PythonAnywhere** (~$25/mes)

### Frontend Alternativas a Vercel
- **Netlify** (gratis, similar a Vercel)
- **GitHub Pages** (solo para sitios estáticos)

---

**¡Felicidades! Tu aplicación está en producción 🎉**

Próximos pasos:
1. Comparte la URL con amigos/reclutadores
2. Agrega a tu portafolio
3. Escala con más features
4. Monitorea logs y performance
