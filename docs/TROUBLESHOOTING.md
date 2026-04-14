# Solución de Problemas

Problemas comunes y cómo resolverlos.

---

## Base de datos

**`Can't connect to MySQL server`**

Verifica que el servicio MySQL está activo y que la URL en `.env` es correcta:

```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/db_name
```

Asegúrate de usar el prefijo `mysql+pymysql://` y no `mysql://` a secas. SQLAlchemy necesita el driver explícito.

**`Access denied for user`**

El usuario no tiene permisos sobre la base de datos. Ejecuta esto en MySQL como root:

```sql
GRANT ALL PRIVILEGES ON db_name.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
```

**`Field 'is_active' doesn't have a default value`**

Estás insertando un registro en la tabla de productos sin ese campo. Incluye `is_active=1` explícitamente en el INSERT, o añade un valor por defecto en la tabla:

```sql
ALTER TABLE products MODIFY COLUMN is_active BOOLEAN DEFAULT 1;
```

**`Unknown database`**

La base de datos no existe. Créala:

```sql
CREATE DATABASE jwt_api CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## Errores JWT

**`401 Unauthorized` / `Could not validate credentials`**

El access token expiró (dura 15 minutos por defecto). Llama a `POST /api/v1/auth/refresh` para obtener uno nuevo usando el refresh token guardado en la cookie `HttpOnly`.

Si tampoco tienes refresh token válido, el usuario tiene que iniciar sesión de nuevo.

**`Token signature verification failed`**

La `SECRET_KEY` cambió entre reinicios. Si está vacía en `.env`, FastAPI genera una aleatoria al arrancar — todos los tokens anteriores quedan inválidos. Define una clave fija en `.env`:

```
SECRET_KEY=una-clave-larga-random-que-no-cambie
```

Genera una buena clave con:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## CORS

**`Access to fetch at '...' has been blocked by CORS policy`**

1. Verifica el valor de `ALLOWED_ORIGINS` en Railway (o tu `.env`). Debe ser exactamente la URL del frontend **sin barra final**:
   ```
   ALLOWED_ORIGINS=https://jwt-api-proyecto-v20.vercel.app
   ```
   Una barra al final (`...app/`) es suficiente para que el navegador rechace la petición.

2. Si el frontend está en otra URL (custom domain, preview deploy), añade esa URL separada por comas:
   ```
   ALLOWED_ORIGINS=https://tudominio.com,https://preview.vercel.app
   ```

3. En desarrollo local el frontend corre en `http://localhost:4321` por defecto. Ese origen ya está incluido en los defaults del backend para `DEBUG=True`.

---

## Frontend (Vercel / Astro)

**Las páginas cargan pero no aparecen datos**

La variable `PUBLIC_API_URL` no está configurada en Vercel, o se cambió después del último build. Astro la incorpora en el momento del build — si no existe en ese momento, las URLs de la API quedan vacías.

Solución:
1. Ve a Vercel → Settings → Environment Variables
2. Añade `PUBLIC_API_URL = https://jwtapiproyecto-production.up.railway.app`
3. Redeploy (un push o un deploy manual desde el dashboard)

**Error de hidratación en la consola (`Hydration mismatch`)**

Ocurre cuando un componente Vue usa `<Teleport>` o `<Transition>` y Astro intenta hidratarlo con SSR. La solución es usar `client:only="vue"` en vez de `client:load`.

Ejemplo en `DashboardLayout.astro`:
```astro
<CommandPalette client:only="vue" />
```

**El directorio raíz de Vercel es incorrecto**

Vercel podría intentar buildear desde la raíz del repo en vez de `frontend/`. Verifica en Vercel → Settings → General → Root Directory que esté apuntando a `frontend`.

---

## Railway (Backend)

**`Application failed to respond`**

Railway inyecta `$PORT` automáticamente. No configures un puerto fijo en las variables de entorno ni en el Procfile. El Procfile debe verse así:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Si ves ese error a pesar de tener el Procfile correcto, revisa los logs de Railway en tiempo real (`Deployments → Ver logs`) para ver el error real.

**El build falla con `ModuleNotFoundError`**

Alguna dependencia falta en `requirements.txt`. Añádela y haz push. Si la dependencia es nueva (por ejemplo, `slowapi`), debe aparecer en `requirements.txt` con la versión exacta.

**`DATABASE_URL` — errores de conexión en producción**

Railway MySQL genera la URL con el prefijo `mysql://`. Cámbialo manualmente a `mysql+pymysql://` en la variable de entorno:

```
DATABASE_URL=mysql+pymysql://root:password@monorail.proxy.rlwy.net:19703/railway
```

---

## Cookies y refresh tokens

**El refresh token no se envía entre dominios**

Las cookies `HttpOnly` con `SameSite=None` requieren HTTPS en ambos extremos. Si el backend está en Railway (`https://`) y el frontend en Vercel (`https://`) funciona correctamente.

Si estás en desarrollo local (HTTP), el navegador puede descartar la cookie. Para pruebas locales completas del flujo de refresh, usa la extensión de Swagger en `http://localhost:8000/docs` o herramientas como Postman que gestionan cookies correctamente.

**El logout no elimina la cookie**

El endpoint `POST /api/v1/auth/logout` limpia la cookie del lado del servidor, pero el frontend también debe eliminar el `access_token` del estado local (localStorage, variable en memoria, etc.).

---

## Otros

**`422 Unprocessable Entity`**

El cuerpo de la petición no cumple la validación del schema de Pydantic. La respuesta incluye el detalle del campo que falló:

```json
{
  "detail": [
    { "loc": ["body", "price"], "msg": "value is not a valid float", "type": "type_error.float" }
  ]
}
```

**`403 Forbidden`**

El usuario está autenticado pero no tiene permiso. Los endpoints de administración requieren `role=admin`. Cambia el rol del usuario vía `PATCH /api/v1/users/{id}/role` con una cuenta admin.

**El servidor tarda mucho en responder la primera vez**

Railway pone los servicios en sleep después de inactividad (plan gratuito). El primer request tras un periodo sin tráfico puede tardar 5-15 segundos mientras el contenedor arranca. Los siguientes son normales.
