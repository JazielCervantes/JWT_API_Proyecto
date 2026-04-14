# Conceptos y arquitectura

Este documento explica las decisiones de diseño detrás del proyecto para que sea más fácil extenderlo o adaptarlo.

---

## Autenticación: JWT con dos tokens

El sistema usa dos tokens con propósitos distintos.

**Access token** (15 minutos)
- Se incluye en cada petición en el header `Authorization: Bearer ...`
- Vida corta intencionalmente: si alguien lo intercepta, expira pronto
- Se guarda en `sessionStorage` y `localStorage` en el navegador

**Refresh token** (7 días)
- Sirve solo para obtener un nuevo access token cuando el anterior expira
- Viaja como HTTP-Only cookie: JavaScript no puede leerlo, solo el servidor lo ve
- Esto lo protege contra ataques XSS

Cuando el frontend recibe un 401, intenta automáticamente renovar el access token usando el refresh token. Si eso también falla (refresh expirado o revocado), redirige al login.

```
Login
  └── Servidor devuelve access_token + refresh_token (en cookie)
        └── Petición con access_token
              └── 401 (expirado)
                    └── POST /auth/refresh con cookie
                          └── Nuevo access_token → reintentar petición
                                ├── OK: continuar
                                └── 401 de nuevo: logout + redirect a login
```

## Roles y autorización

Hay dos roles: `admin` y `user`. La diferencia en la práctica:

| Acción | user | admin |
|---|---|---|
| Ver productos | Sí | Sí |
| Crear/editar/eliminar productos | No | Sí |
| Ver lista de usuarios | No | Sí |
| Cambiar roles de usuarios | No | Sí |
| Ver su propio perfil | Sí | Sí |

La autorización se verifica en el backend en cada endpoint. El frontend solo oculta botones por comodidad visual, pero la restricción real está en el servidor.

## Estructura del backend

El backend sigue un patrón de capas clásico:

```
Route (HTTP) → Service (lógica) → Repository (BD) → Model (SQLAlchemy)
```

**Routes** (`app/routes/`): Reciben la petición HTTP, validan con Pydantic y delegan al service. No tienen lógica de negocio.

**Services** (`app/services/`): Contienen la lógica de negocio (verificar credenciales, generar tokens, etc.).

**Repositories** (`app/repositories/`): Toda interacción con la base de datos pasa por aquí. El resto del código no usa SQLAlchemy directamente.

**Models** (`app/models/`): Definición de tablas con SQLAlchemy ORM.

**Schemas** (`app/schemas/`): Modelos Pydantic para validar entrada y serializar salida.

La idea es que si mañana cambias MySQL por PostgreSQL, solo tocas el repository y el `DATABASE_URL`. El resto del código no se entera.

## Versionamiento de API

Todos los endpoints están bajo `/api/v1/`. Aunque actualmente solo existe v1, la estructura ya está preparada para agregar v2 sin romper clientes existentes.

```
/api/v1/auth/login
/api/v1/users/
/api/v1/products/
```

El archivo `app/utils/api_versioning.py` tiene un `APIVersionManager` que facilita registrar múltiples versiones si llegara a necesitarse.

## Frontend: Astro con islas Vue

Astro genera páginas estáticas y solo hidrata los componentes que necesitan interactividad en el cliente. En este proyecto:

- **ThemeToggle.vue**: usa `client:load` porque necesita acceso a `localStorage` y `document` desde el primer render
- **CommandPalette.vue**: usa `client:only="vue"` porque usa `<Teleport to="body">`, que no puede pre-renderizarse en servidor sin causar hydration mismatches

El resto de la lógica (fetch de datos, DOM manipulation) va en `<script>` inline de Astro, que se ejecuta como JavaScript normal en el cliente después de que la página carga.

## Seguridad: qué está implementado

- **bcrypt** para hash de contraseñas con salt único por usuario
- **HTTP-Only cookies** para el refresh token (inaccessible desde JS)
- **Security headers** en todas las respuestas: `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`, `Content-Security-Policy`
- **Rate limiting** con `slowapi`: 5 intentos de login por minuto, 3 registros por hora
- **CORS** configurado explícitamente, no con `*` en producción
- **DEBUG=False** en producción para no exponer stack traces en errores 500
- **Validación de entrada** con Pydantic en todos los endpoints

## Variables de entorno importantes

| Variable | Propósito | Notas |
|---|---|---|
| `SECRET_KEY` | Firmar los JWT | Debe ser aleatoria y larga (mínimo 32 chars) |
| `DEBUG` | Modo debug | `True` en desarrollo, `False` en producción siempre |
| `ALLOWED_ORIGINS` | CORS | Solo el dominio real en producción, no `*` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Vida del access token | 15 minutos es el balance justo entre usabilidad y seguridad |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Vida del refresh token | 7 días, después el usuario debe hacer login de nuevo |
