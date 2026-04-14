# API REST con JWT + Frontend SaaS

![Version](https://img.shields.io/badge/version-2.0.0-indigo)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green)
![Astro](https://img.shields.io/badge/Astro-4.2-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

Proyecto full-stack con backend FastAPI y frontend Astro. Incluye autenticación JWT completa, sistema de roles, CRUD de productos y un panel de administración con diseño minimalista estilo SaaS.

## Lo que incluye

**Backend (FastAPI)**
- Autenticación JWT con access tokens (15 min) y refresh tokens (7 días) en HTTP-Only cookies
- Sistema de roles: Admin y User, con middleware de autorización por endpoint
- CRUD completo de productos y usuarios con paginación y filtros
- Rate limiting (5 intentos de login por minuto, 3 registros por hora)
- Security headers, CORS configurado y hash bcrypt de contraseñas
- Repository Pattern con inyección de dependencias
- Documentación automática en `/docs` (Swagger) y `/redoc`

**Frontend (Astro + Vue + TailwindCSS)**
- Diseño minimalista SaaS con modo claro y oscuro
- Command palette con Ctrl+K para navegación rápida
- Sidebar responsive con layout de dashboard
- Skeleton loaders en todas las vistas de datos
- Gestión automática de tokens (retry con refresh en 401)

## Stack

| Capa | Tecnología |
|---|---|
| Backend | FastAPI 0.115.6, Python 3.10+ |
| Base de datos | MySQL 8 + SQLAlchemy 2 |
| Autenticación | JWT (python-jose), bcrypt |
| Frontend | Astro 4.2, Vue 3.4, TailwindCSS 3.4 |
| Despliegue | Railway (backend + DB) + Vercel (frontend) |

## Estructura del proyecto

```
jwt-api-project/
├── backend/
│   ├── app/
│   │   ├── core/           # Logging, excepciones, constantes
│   │   ├── middleware/     # Security headers, rate limiting
│   │   ├── models/         # SQLAlchemy (User, Product)
│   │   ├── repositories/   # Capa de acceso a datos
│   │   ├── routes/         # Endpoints /api/v1/
│   │   ├── schemas/        # Validación con Pydantic
│   │   ├── services/       # Lógica de negocio
│   │   ├── utils/          # JWT, seguridad, dependencias
│   │   ├── main.py
│   │   ├── config.py
│   │   └── database.py
│   ├── docs/
│   │   └── EJEMPLOS_USO.md
│   ├── requirements.txt
│   ├── railway.json
│   └── Procfile
├── frontend/
│   ├── src/
│   │   ├── components/     # ThemeToggle, CommandPalette
│   │   ├── layouts/        # Layout.astro, DashboardLayout.astro
│   │   ├── lib/            # api.js, auth.js
│   │   ├── pages/          # index, login, register, dashboard, products, users, profile
│   │   └── styles/
│   ├── vercel.json
│   └── package.json
├── docs/
│   ├── DEPLOYMENT.md
│   ├── DEVELOPMENT.md
│   ├── EXAMPLES.md
│   └── TROUBLESHOOTING.md
├── seed_products.py
├── INSTALLATION.md
└── README.md
```

## Inicio rápido (local)

Necesitas Python 3.10+, Node.js 18+ y MySQL 8.

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux
pip install -r requirements.txt
cp .env.example .env        # Editar con tus credenciales de MySQL
uvicorn app.main:app --reload

# Frontend (otra terminal)
cd frontend
npm install
cp .env.example .env        # PUBLIC_API_URL=http://localhost:8000
npm run dev
```

- Frontend: http://localhost:4321
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Login inicial: `admin` / `admin123`

Lee [INSTALLATION.md](INSTALLATION.md) para la guía completa paso a paso.

## Despliegue

El proyecto está configurado para desplegarse en **Railway** (backend + MySQL) y **Vercel** (frontend). Ver [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) para instrucciones detalladas.

## Versiones

### v2.0.0 (actual)
- Rediseño completo del frontend: diseño SaaS minimalista, modo oscuro/claro
- Nuevo layout con sidebar fijo y navbar sticky
- Command palette (Ctrl+K), skeleton loaders, componentes Vue reactivos
- Configuración de despliegue para Vercel y Railway
- `DEBUG=False` por defecto en producción
- `slowapi` añadido a requirements

### v1.0.0
- Backend FastAPI con JWT, roles, rate limiting, security headers
- Frontend con tema glassmorphism oscuro
- Repository Pattern, CRUD completo

## Licencia

MIT
