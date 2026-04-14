# Despliegue a producción

El proyecto usa **Railway** para el backend y la base de datos, y **Vercel** para el frontend. Ambos tienen planes gratuitos suficientes para este tipo de proyecto.

---

## Antes de empezar

Necesitas:
- El código subido a un repositorio de GitHub
- Cuenta en [railway.app](https://railway.app) (login con GitHub)
- Cuenta en [vercel.com](https://vercel.com) (login con GitHub)

---

## Paso 1: Desplegar el backend en Railway

### Crear el proyecto

1. En Railway, click en **New Project** → **Deploy from GitHub repo**
2. Selecciona tu repositorio
3. Railway detectará el monorepo. Cuando pregunte por el directorio raíz, escribe `backend`

### Agregar MySQL

1. Dentro del proyecto, click en **+ New** → **Database** → **MySQL**
2. Railway crea la base de datos automáticamente
3. Ve al servicio MySQL → pestaña **Connect** → copia la `DATABASE_URL`
4. Cambia el prefijo de `mysql://` a `mysql+pymysql://` en la URL copiada (PyMySQL lo necesita)

### Configurar variables de entorno

Ve a tu servicio backend → **Variables** → agrega cada una:

| Variable | Valor |
|---|---|
| `DATABASE_URL` | La URL de MySQL con prefijo `mysql+pymysql://` |
| `SECRET_KEY` | Genera una con `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `15` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` |
| `APP_VERSION` | `2.0.0` |
| `DEBUG` | `False` |
| `ALLOWED_ORIGINS` | Lo actualizarás después con la URL de Vercel |
| `ADMIN_EMAIL` | El email que quieras para el admin |
| `ADMIN_USERNAME` | `admin` (o el que prefieras) |
| `ADMIN_PASSWORD` | Una contraseña segura, no uses `admin123` en producción |
| `ADMIN_FULL_NAME` | El nombre que quieras |

### Verificar el deploy

Railway redespliega automáticamente al guardar variables. Espera que el build termine y visita:

```
https://tu-backend.up.railway.app/health
```

Debería responder `{"status":"healthy","version":"2.0.0"}`. Si ves eso, el backend está listo.

La documentación de la API queda en `https://tu-backend.up.railway.app/docs`.

---

## Paso 2: Desplegar el frontend en Vercel

### Crear el proyecto

1. En Vercel, click en **Add New...** → **Project**
2. Importa tu repositorio de GitHub
3. Configura estos campos:
   - **Framework Preset**: Astro
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (detectado automáticamente)
   - **Output Directory**: `dist` (detectado automáticamente)

### Variable de entorno

Antes de hacer Deploy, en la sección **Environment Variables**:

| Variable | Valor |
|---|---|
| `PUBLIC_API_URL` | `https://tu-backend.up.railway.app` (sin `/` al final) |

Click **Deploy** y espera 2-3 minutos.

---

## Paso 3: Conectar ambos servicios

Una vez que Vercel termina el deploy, tienes la URL del frontend (algo como `https://tu-proyecto.vercel.app`).

Vuelve a **Railway** → tu servicio backend → **Variables** → edita `ALLOWED_ORIGINS`:

```
https://tu-proyecto.vercel.app
```

Si quieres mantener también acceso desde local:

```
https://tu-proyecto.vercel.app,http://localhost:4321
```

Railway redespliega en cuanto guardas. Espera un minuto y prueba el login desde Vercel.

---

## Paso 4: Cargar datos iniciales (opcional)

Si quieres poblar la base de datos con productos de ejemplo, ejecuta desde tu terminal local:

```bash
python seed_products.py "mysql+pymysql://USER:PASS@HOST:PORT/railway"
```

Usa la misma `DATABASE_URL` que pusiste en Railway (la que contiene `monorail.proxy.rlwy.net`).

---

## Checklist antes de dar el deploy por terminado

**Seguridad**
- [ ] `SECRET_KEY` es una clave generada aleatoriamente (no un texto fijo)
- [ ] `ADMIN_PASSWORD` no es `admin123`
- [ ] `DEBUG=False`
- [ ] `ALLOWED_ORIGINS` solo contiene el dominio de Vercel, no `*`

**Funcionalidad**
- [ ] `/health` responde correctamente
- [ ] Login funciona desde el frontend en Vercel
- [ ] El dashboard carga los productos
- [ ] El CRUD de productos funciona
- [ ] El logout redirige al login

---

## Actualizaciones futuras

Cada vez que hagas push a la rama principal de GitHub:
- Vercel redespliega el frontend automáticamente
- Railway redespliega el backend automáticamente

No necesitas hacer nada manual después del setup inicial.

---

## Solución de problemas comunes

**"Application failed to respond" en Railway:** El puerto está mal configurado. No ingreses el puerto 8000 manualmente. Railway asigna el puerto via `$PORT` automáticamente — no toques esa configuración.

**Error de CORS al hacer login:** `ALLOWED_ORIGINS` no tiene la URL exacta de Vercel. Asegúrate de que no tenga `/` al final y que sea `https://` (nunca `http://`).

**`DATABASE_URL` no funciona:** Verifica que el prefijo sea `mysql+pymysql://` y no `mysql://`. Railway exporta el formato estándar que PyMySQL no entiende directamente.

**El frontend muestra localhost en producción:** La variable `PUBLIC_API_URL` no se configuró antes del build. Las variables de Astro se embeben en el momento del build, no en runtime. Cambia la variable en Vercel y haz un nuevo deploy.
