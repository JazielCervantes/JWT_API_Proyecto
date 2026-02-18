# 🚀 Despliegue en Vercel (Frontend)

## 📋 ¿Qué es Vercel?

Vercel es la plataforma perfecta para desplegar aplicaciones Astro, Next.js, y otros frameworks modernos. Es **GRATIS** para proyectos personales.

### ✨ Ventajas

- ✅ **Gratis** para proyectos personales
- ✅ **SSL automático** (HTTPS)
- ✅ **CDN global** (muy rápido)
- ✅ **Deploy automático** desde GitHub
- ✅ **Vista previa** de pull requests
- ✅ **Dominio personalizado** gratis

---

## 🎯 Requisitos Previos

- ✅ Código en GitHub (ver `GITHUB_SETUP.md`)
- ✅ Frontend funcionando localmente
- ✅ Cuenta de GitHub

---

## 📋 Paso a Paso

### 1. Crear Cuenta en Vercel

1. Ve a https://vercel.com
2. Click en **Sign Up**
3. Selecciona **Continue with GitHub**
4. Autoriza a Vercel para acceder a tus repositorios

---

### 2. Importar Proyecto

1. Click en **Add New...** → **Project**
2. Busca tu repositorio `jwt-api-project`
3. Click en **Import**

---

### 3. Configurar el Proyecto

#### General Settings

```
Project Name: jwt-api-frontend
Framework Preset: Astro
Root Directory: frontend/
```

#### Build & Output Settings

```
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

#### Environment Variables

Click en **Environment Variables** y agrega:

```
Name: PUBLIC_API_URL
Value: https://tu-api-en-railway.railway.app
```

> **Nota**: Primero despliega el backend (ver `DESPLIEGUE_RAILWAY.md`) y luego vuelve aquí con la URL real.

---

### 4. Desplegar

1. Click en **Deploy**
2. Espera 1-2 minutos
3. ✅ ¡Tu frontend está en línea!

Tu app estará disponible en: `https://tu-proyecto.vercel.app`

---

## 🔧 Configuración Avanzada

### Actualizar Variables de Entorno

1. Ve a tu proyecto en Vercel
2. **Settings** → **Environment Variables**
3. Edita `PUBLIC_API_URL` con la URL real de tu backend
4. Click **Save**
5. Ve a **Deployments** → Click en el último deploy → **Redeploy**

---

### Dominio Personalizado

#### Usar dominio propio

1. **Settings** → **Domains**
2. Ingresa tu dominio: `miapp.com`
3. Sigue las instrucciones para configurar DNS:
   ```
   Type: CNAME
   Name: @
   Value: cname.vercel-dns.com
   ```

#### Subdominio

Para `app.miapp.com`:
```
Type: CNAME
Name: app
Value: cname.vercel-dns.com
```

---

### Deploys Automáticos

Vercel despliega automáticamente cuando haces push a GitHub:

```bash
# Hacer cambios en el frontend
cd frontend
# ... editar archivos ...

# Commit y push
git add .
git commit -m "feat: mejorar diseño del login"
git push

# Vercel detecta el cambio y despliega automáticamente
```

---

### Vista Previa de Pull Requests

Cada PR obtiene su propia URL de preview:

1. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
2. Haz cambios y push: `git push -u origin feature/nueva-funcionalidad`
3. Crea Pull Request en GitHub
4. Vercel comenta con URL de preview: `https://jwt-api-frontend-git-feature-nueva-tu-usuario.vercel.app`
5. Prueba la vista previa
6. Si todo está bien, haz merge

---

## 🔒 Configuración de Seguridad

### Headers de Seguridad

Crea `vercel.json` en la raíz del frontend:

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        }
      ]
    }
  ]
}
```

---

### CORS en el Backend

Asegúrate de que tu backend permita requests desde Vercel.

En `backend/app/.env`:
```env
ALLOWED_ORIGINS=https://tu-proyecto.vercel.app,https://*.vercel.app
```

En `backend/app/config.py`:
```python
ALLOWED_ORIGINS: str = "https://tu-proyecto.vercel.app,https://*.vercel.app"
```

---

## 📊 Monitoreo

### Analytics (Gratis en plan Hobby)

1. **Settings** → **Analytics**
2. Enable Analytics
3. Ver estadísticas:
   - Visitas
   - Ubicación geográfica
   - Dispositivos
   - Performance

### Logs

1. Ve a tu proyecto
2. Click en el deployment actual
3. **Functions** tab → Ver logs en tiempo real

---

## ⚡ Optimizaciones

### Cache de Build

Vercel cachea automáticamente `node_modules`. Para limpiar:

1. **Settings** → **General**
2. Scroll hasta "Build Cache"
3. Click **Clear Build Cache**

### Configurar Redirects

En `vercel.json`:

```json
{
  "redirects": [
    {
      "source": "/old-path",
      "destination": "/new-path",
      "permanent": true
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://tu-backend.railway.app/api/:path*"
    }
  ]
}
```

---

## 🚨 Troubleshooting

### Build Failed

**Error común**: `Command "npm run build" exited with 1`

**Solución**:
1. Verifica que el proyecto compile localmente:
   ```bash
   cd frontend
   npm run build
   ```
2. Revisa los logs en Vercel
3. Asegúrate de que `ROOT_DIRECTORY` sea `frontend/`

---

### Environment Variables no se aplican

**Solución**:
1. Agrega las variables
2. **Deployments** → último deploy → **Redeploy**
3. Marca "Use existing Build Cache" como **OFF**

---

### Error de CORS

**Error**: `Access to fetch... has been blocked by CORS policy`

**Solución en el backend**:

```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tu-proyecto.vercel.app",
        "https://*.vercel.app"  # Para preview deploys
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Reinicia el backend después de este cambio.

---

### Página 404 en rutas

Astro genera páginas estáticas. Si usas client-side routing, crea `vercel.json`:

```json
{
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

---

## 💰 Planes y Límites

### Plan Hobby (Gratis)

- ✅ Proyectos ilimitados
- ✅ SSL automático
- ✅ 100 GB bandwidth/mes
- ✅ 1000 build minutes/mes
- ✅ Deployments ilimitados
- ⚠️ 1 miembro del equipo

### Si necesitas más

- **Pro** ($20/mes): Para equipos y proyectos comerciales
- **Enterprise**: Contacto personalizado

Para proyectos personales y portafolios, el plan gratuito es más que suficiente.

---

## 📱 Vercel App Móvil

1. Descarga la app de Vercel (iOS/Android)
2. Recibe notificaciones de deploys
3. Ver analytics
4. Manage deployments

---

## ✅ Checklist de Despliegue

Antes de desplegar:

- [ ] `npm run build` funciona localmente
- [ ] Variables de entorno configuradas
- [ ] URL del backend correcta en `PUBLIC_API_URL`
- [ ] CORS configurado en el backend
- [ ] `.gitignore` incluye `.env`
- [ ] Root directory configurado como `frontend/`

---

## 🎯 Próximos Pasos

1. ✅ Frontend desplegado en Vercel
2. 🔗 Obtener URL del frontend
3. 📝 Actualizar README con link del demo
4. 🎨 Probar la app en producción

**Siguiente**: Despliega el backend (ver `DESPLIEGUE_RAILWAY.md`)

---

## 📚 Recursos

- [Vercel Docs](https://vercel.com/docs)
- [Astro Deploy Guide](https://docs.astro.build/en/guides/deploy/vercel/)
- [Vercel CLI](https://vercel.com/docs/cli)

---

## 💡 Tips Pro

### Deploy desde la CLI

```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Deploy a producción
vercel --prod
```

### Variables de Entorno por Ambiente

Puedes tener diferentes valores para:
- **Production**: URL real del backend
- **Preview**: URL de staging
- **Development**: localhost

Configurar en **Settings** → **Environment Variables** → Seleccionar el ambiente.

---

¡Tu frontend ahora está en producción! 🎉

**URL de ejemplo**: https://jwt-api-frontend.vercel.app/
