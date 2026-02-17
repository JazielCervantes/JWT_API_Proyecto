# 🚂 Despliegue en Railway (Backend)

## 📋 ¿Qué es Railway?

Railway es una plataforma moderna para desplegar aplicaciones backend. Perfecto para FastAPI + MySQL.

### ✨ Ventajas

- ✅ **$5 gratis al mes** (suficiente para proyectos pequeños)
- ✅ **MySQL incluido** (no necesitas configurar)
- ✅ **SSL automático**
- ✅ **Deploy desde GitHub**
- ✅ **Logs en tiempo real**
- ✅ **Fácil de usar**

---

## 🎯 Requisitos Previos

- ✅ Código en GitHub
- ✅ Backend funcionando localmente
- ✅ Cuenta de GitHub

---

## 📋 Paso a Paso

### 1. Crear Cuenta en Railway

1. Ve a https://railway.app
2. Click en **Login**
3. Selecciona **Login with GitHub**
4. Autoriza Railway

---

### 2. Crear Nuevo Proyecto

1. Click en **New Project**
2. Selecciona **Deploy from GitHub repo**
3. Busca `jwt-api-project`
4. Click en el repositorio

---

### 3. Configurar el Servicio Backend

1. Railway detectará tu proyecto
2. Click en **Add variables** (o configúralas después)

#### Variables de Entorno Requeridas

```env
# Base de datos (Railway la creará automáticamente)
DATABASE_URL=${{MySQL.DATABASE_URL}}

# Seguridad
SECRET_KEY=genera_una_clave_super_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# App
APP_NAME=JWT API
DEBUG=False

# CORS - Actualizarás después con la URL de Vercel
ALLOWED_ORIGINS=https://tu-proyecto.vercel.app,http://localhost:4321

# Admin
ADMIN_EMAIL=admin@ejemplo.com
ADMIN_USERNAME=admin
ADMIN_PASSWORD=cambia_esto_por_password_seguro
```

---

### 4. Agregar Base de Datos MySQL

1. En el proyecto, click en **+ New**
2. Selecciona **Database** → **Add MySQL**
3. Railway crea automáticamente una base de datos
4. La variable `DATABASE_URL` se configura automáticamente

---

### 5. Configurar Despliegue

#### Crear archivo `railway.json` en la raíz del proyecto:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "cd backend && pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### O configurar manualmente:

**Settings** → **Deploy**:
```
Root Directory: backend/
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

### 6. Generar SECRET_KEY Segura

```bash
# En tu terminal local
python -c "import secrets; print(secrets.token_hex(32))"
```

Copia el resultado y pégalo en la variable `SECRET_KEY` en Railway.

---

### 7. Desplegar

1. Click en **Deploy** (o se despliega automáticamente)
2. Espera 2-3 minutos
3. ✅ ¡Tu backend está en línea!

---

### 8. Obtener URL del Backend

1. Ve a **Settings** → **Networking**
2. Click en **Generate Domain**
3. Obtendrás algo como: `jwt-api-backend.up.railway.app`

---

### 9. Inicializar Base de Datos

#### Opción A: Ejecutar script desde Railway

1. Ve a **Variables** 
2. Asegúrate de que todas estén configuradas
3. El backend creará las tablas automáticamente al iniciar

#### Opción B: Conectarte directamente a MySQL

Railway te da las credenciales de MySQL:

```
Host: containers-us-west-xxx.railway.app
Port: 5432
Database: railway
User: root
Password: [ver en Railway]
```

Conéctate con MySQL Workbench o CLI:

```bash
mysql -h containers-us-west-xxx.railway.app -P 5432 -u root -p
```

Ejecuta:
```sql
USE railway;
SHOW TABLES;
```

---

### 10. Verificar que Funciona

Accede a tu API:

```
https://tu-backend.railway.app/docs
```

Deberías ver la documentación Swagger.

---

## 🔧 Configuración Avanzada

### Actualizar CORS

Una vez tengas la URL de Vercel, actualiza:

**Variables** en Railway:
```env
ALLOWED_ORIGINS=https://tu-proyecto.vercel.app,https://*.vercel.app
```

**Redeploy** para aplicar cambios.

---

### Logs en Tiempo Real

1. Ve a tu servicio en Railway
2. Click en **Deployments**
3. Ver logs en tiempo real
4. Útil para debugging

---

### Configurar Health Checks

Railway verifica automáticamente que tu app esté viva.

En `backend/app/main.py` ya tienes:
```python
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

Railway usa esto para verificar el estado.

---

### Escalado

**Plan Hobby ($5 gratis/mes)**:
- 500 MB RAM
- 1 vCPU
- 5 GB almacenamiento
- 100 GB bandwidth

Si necesitas más, upgradea a:
- **Developer** ($10/mes): 8 GB RAM
- **Team** ($20/mes): Colaboración

---

## 🗄️ Backups de Base de Datos

### Hacer Backup Manual

```bash
# Conectarte a MySQL de Railway
mysql -h HOST -P PORT -u root -p railway > backup.sql

# O con mysqldump
mysqldump -h HOST -P PORT -u root -p railway > backup.sql
```

### Backup Automático

Railway hace backups automáticos en planes pagos. Para el plan gratuito:

1. Crea un script de backup
2. Usa GitHub Actions para ejecutarlo periódicamente
3. Guarda en GitHub o S3

---

## 🔒 Seguridad en Producción

### Checklist de Seguridad

- [ ] `DEBUG=False` en producción
- [ ] `SECRET_KEY` única y segura (32+ caracteres)
- [ ] Contraseña de admin cambiada
- [ ] CORS configurado correctamente
- [ ] HTTPS habilitado (automático en Railway)
- [ ] Variables de entorno nunca en el código
- [ ] Logs revisados periódicamente

---

### Variables de Entorno Sensibles

**NUNCA** incluyas en el código:
- ❌ Contraseñas
- ❌ API keys
- ❌ SECRET_KEY
- ❌ Tokens

Usa siempre Variables de Entorno en Railway.

---

## 📊 Monitoreo

### Métricas de Railway

1. **Deployments** → Ver historial
2. **Metrics** → CPU, RAM, Network
3. **Logs** → Errores y warnings

### Alertas

Railway no tiene alertas built-in en el plan gratuito. Para monitoreo avanzado:

1. Usa **Sentry** (errores)
2. Usa **Uptime Robot** (disponibilidad)
3. Usa **Papertrail** (logs centralizados)

---

## 🚨 Troubleshooting

### Build Failed

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solución**:
1. Verifica `railway.json` o configuración de deploy
2. Asegúrate de que `Root Directory` sea `backend/`
3. `Build Command` debe instalar dependencias
4. `Start Command` debe incluir `cd backend`

---

### Application Error

**Error**: Página muestra "Application Error"

**Solución**:
1. Ver logs: **Deployments** → último deploy → **View Logs**
2. Buscar el error específico
3. Verificar variables de entorno
4. Asegurarse de que `PORT` se use correctamente:
   ```python
   # En main.py
   if __name__ == "__main__":
       import os
       port = int(os.environ.get("PORT", 8000))
       uvicorn.run("app.main:app", host="0.0.0.0", port=port)
   ```

---

### Database Connection Failed

**Error**: `Can't connect to MySQL server`

**Solución**:
1. Verifica que el servicio MySQL esté corriendo
2. **Variables** → Verifica `DATABASE_URL`
3. Debe ser algo como:
   ```
   mysql+pymysql://root:password@containers.railway.app:3306/railway
   ```

---

### CORS Error

**Error**: `Access to fetch... has been blocked by CORS`

**Solución**:
1. Actualiza `ALLOWED_ORIGINS` en Railway
2. Incluye la URL de Vercel
3. Incluye `https://*.vercel.app` para preview deploys
4. Redeploy

---

## 💰 Costos y Límites

### Plan Hobby (Gratis)

- ✅ $5 gratis al mes
- ✅ 500 horas de ejecución
- ✅ Sin tarjeta de crédito requerida
- ⚠️ Sleeps después de inactividad

**Para mantenerlo activo 24/7**:

1. Usa **Uptime Robot** (gratis)
2. Configura ping cada 5 minutos a `/health`
3. Railway no dormirá tu app

### Si se acaban los $5

Opciones:
1. **Pagar**: Agregar tarjeta de crédito
2. **Optimizar**: Reducir uso de recursos
3. **Alternativas**: Render, Fly.io, Heroku

---

## 🔄 Deploy Automático

Railway despliega automáticamente cuando haces push:

```bash
# Hacer cambios en backend
cd backend
# ... editar archivos ...

git add .
git commit -m "fix: corregir bug en autenticación"
git push

# Railway detecta el cambio y despliega automáticamente
```

---

## 🎯 Alternativa: Render

Si Railway no funciona para ti, prueba **Render**:

### Ventajas de Render
- ✅ Gratis permanente (con limitaciones)
- ✅ No sleeps después de 15 min (en plan pagado)
- ✅ PostgreSQL gratis (SQLite en plan gratuito)

### Configuración en Render

```yaml
# render.yaml
services:
  - type: web
    name: jwt-api-backend
    env: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
```

---

## ✅ Checklist de Despliegue

- [ ] Cuenta en Railway creada
- [ ] Proyecto conectado a GitHub
- [ ] MySQL agregado
- [ ] Variables de entorno configuradas
- [ ] SECRET_KEY generada y segura
- [ ] Contraseña de admin cambiada
- [ ] Deploy exitoso
- [ ] `/docs` funciona
- [ ] Login funciona
- [ ] CORS configurado con URL de Vercel

---

## 🎯 Próximos Pasos

1. ✅ Backend desplegado en Railway
2. 🔗 URL del backend: `https://tu-backend.railway.app`
3. ↩️ Volver a Vercel y actualizar `PUBLIC_API_URL`
4. 🎉 ¡App completa en producción!

---

## 📚 Recursos

- [Railway Docs](https://docs.railway.app/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Railway Templates](https://railway.app/templates)

---

¡Tu backend ahora está en producción! 🚂

**URL de ejemplo**: https://jwt-api-backend.up.railway.app
