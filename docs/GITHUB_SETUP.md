# 📤 Guía Completa: Subir Proyecto a GitHub

## 🎯 Objetivo

Subir tu proyecto completo a GitHub de forma segura, sin exponer datos sensibles.

---

## ⚠️ IMPORTANTE: Seguridad Primero

### Archivos que NUNCA debes subir:

- ❌ `.env` (contiene contraseñas y secretos)
- ❌ `venv/` o `node_modules/` (dependencias)
- ❌ `__pycache__/` (archivos temporales Python)
- ❌ `dist/` o `build/` (archivos compilados)
- ❌ Tokens o API keys
- ❌ Contraseñas de bases de datos

---

## 📋 Paso a Paso

### 1. Preparar el Proyecto

#### Verificar .gitignore

Tu proyecto ya incluye un `.gitignore`, pero verifica que tenga esto:

```gitignore
# Python
__pycache__/
*.py[cod]
venv/
.env

# Node
node_modules/
.env
dist/
build/

# IDEs
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite3
```

#### Verificar que .env no se suba

```bash
# Desde la raíz del proyecto
git status

# NO debes ver .env en la lista
# Si aparece, agrégalo al .gitignore:
echo ".env" >> .gitignore
echo "backend/.env" >> .gitignore
echo "frontend/.env" >> .gitignore
```

---

### 2. Crear Repositorio en GitHub

#### Opción A: Desde GitHub.com

1. Ve a https://github.com
2. Click en el **+** (arriba derecha) → **New repository**
3. Configura:
   - **Repository name**: `jwt-api-project` (o tu nombre preferido)
   - **Description**: "API REST profesional con JWT, roles y frontend Astro"
   - **Visibility**: 
     - ✅ **Public** - Todos pueden ver (recomendado para portafolio)
     - 🔒 **Private** - Solo tú puedes ver
   - **NO** marques "Initialize with README" (ya tienes uno)
4. Click **Create repository**

#### Opción B: Desde GitHub CLI (gh)

```bash
gh repo create jwt-api-project --public --source=. --remote=origin
```

---

### 3. Configurar Git Localmente

#### Inicializar Git (si no lo has hecho)

```bash
# Ir a la raíz del proyecto
cd jwt-api-project

# Inicializar repositorio
git init

# Configurar tu identidad (si es primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

#### Ver qué archivos se van a subir

```bash
git status
```

**Verifica que NO aparezcan:**
- ❌ `.env`
- ❌ `venv/`
- ❌ `node_modules/`
- ❌ `__pycache__/`

---

### 4. Hacer el Primer Commit

```bash
# Agregar todos los archivos
git add .

# Verificar qué se agregó
git status

# Crear commit
git commit -m "Initial commit: API REST con JWT + Frontend Astro"
```

---

### 5. Conectar con GitHub

```bash
# Agregar el repositorio remoto
# Reemplaza TU_USUARIO con tu nombre de usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/jwt-api-project.git

# Verificar que se agregó correctamente
git remote -v
```

---

### 6. Subir el Código

```bash
# Primera vez (crear rama main y subir)
git branch -M main
git push -u origin main

# Siguiente veces (solo subir cambios)
git push
```

---

## 🔐 Configurar Secrets en GitHub

GitHub Actions y despliegues necesitan acceso a tus secrets. Aquí los configuramos de forma segura.

### 1. Ir a Settings del Repositorio

```
Tu Repositorio → Settings → Secrets and variables → Actions
```

### 2. Agregar Secrets

Click en **New repository secret** y agrega cada uno:

#### Para el Backend:

```
Name: DATABASE_URL
Value: mysql+pymysql://usuario:password@host:3306/jwt_api_db

Name: SECRET_KEY
Value: [Genera uno nuevo con: openssl rand -hex 32]

Name: ADMIN_PASSWORD
Value: tu_password_seguro_para_admin
```

#### Para el Frontend:

```
Name: PUBLIC_API_URL
Value: https://tu-api.railway.app (URL de producción)
```

---

## 📝 Documentar el Proyecto

### Actualizar README.md

Agrega badges e información de despliegue:

```markdown
# JWT API Project

![GitHub](https://img.shields.io/github/license/TU_USUARIO/jwt-api-project)
![GitHub stars](https://img.shields.io/github/stars/TU_USUARIO/jwt-api-project)

## 🚀 Demo

- **Frontend**: https://tu-app.vercel.app
- **API**: https://tu-api.railway.app
- **Docs**: https://tu-api.railway.app/docs

## 📸 Screenshots

[Agregar capturas de pantalla]

## 🛠️ Tecnologías

- Backend: FastAPI, SQLAlchemy, JWT, MySQL
- Frontend: Astro, Vue.js, TailwindCSS

## 🚀 Despliegue

Ver guías en `/docs`:
- DESPLIEGUE_VERCEL.md (frontend)
- DESPLIEGUE_RAILWAY.md (backend)
```

---

## 🔄 Workflow de Trabajo

### Hacer Cambios y Subirlos

```bash
# 1. Ver qué cambió
git status

# 2. Agregar cambios
git add .

# 3. Commit con mensaje descriptivo
git commit -m "feat: agregar página de perfil"

# 4. Subir a GitHub
git push
```

### Tipos de Commits (Convención)

```bash
git commit -m "feat: agregar nueva funcionalidad"
git commit -m "fix: corregir bug en login"
git commit -m "docs: actualizar README"
git commit -m "style: mejorar diseño del dashboard"
git commit -m "refactor: reorganizar componentes"
git commit -m "test: agregar tests unitarios"
```

---

## 🌿 Trabajar con Ramas

### Crear rama para nueva funcionalidad

```bash
# Crear y cambiar a nueva rama
git checkout -b feature/nueva-funcionalidad

# Hacer cambios...
git add .
git commit -m "feat: agregar nueva funcionalidad"

# Subir rama a GitHub
git push -u origin feature/nueva-funcionalidad
```

### Crear Pull Request

1. Ve a tu repositorio en GitHub
2. Verás banner "Compare & pull request"
3. Describe los cambios
4. Click "Create pull request"
5. Después de revisar, haz merge

### Volver a la rama principal

```bash
git checkout main
git pull  # Traer cambios de GitHub
```

---

## 🚨 Problemas Comunes

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/jwt-api-project.git
```

### Error: "Updates were rejected"

```bash
# Traer cambios primero
git pull origin main --rebase
git push
```

### Subiste .env por error

```bash
# Eliminar del repositorio (pero mantener local)
git rm --cached .env
git rm --cached backend/.env
git commit -m "fix: remove .env files"
git push

# Cambiar TODOS los secrets expuestos
# Generar nuevos SECRET_KEY, passwords, etc.
```

### Archivo muy grande

GitHub tiene límite de 100MB por archivo. Si subes algo más grande:

```bash
# Ver archivos grandes
git ls-files -s | sort -k 4 -nr | head -10

# Agregar al .gitignore
echo "archivo-grande.zip" >> .gitignore

# Remover del historial
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch archivo-grande.zip" \
  --prune-empty --tag-name-filter cat -- --all
```

---

## ✅ Checklist de Seguridad

Antes de hacer push, verifica:

- [ ] `.env` está en `.gitignore`
- [ ] No hay contraseñas en el código
- [ ] `venv/` y `node_modules/` están ignorados
- [ ] SECRET_KEY de producción es diferente a desarrollo
- [ ] Las credenciales de admin son seguras
- [ ] `.env.example` NO contiene valores reales
- [ ] Has revisado `git status` antes de commit

---

## 📊 GitHub Actions (Opcional)

### Crear workflow para CI/CD

Crea `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest
```

---

## 🎯 Próximos Pasos

1. ✅ Código en GitHub
2. 📝 README actualizado
3. 🔐 Secrets configurados
4. 🚀 Listo para desplegar

**Siguiente paso**: Ver `DESPLIEGUE_VERCEL.md` para desplegar el frontend.

---

## 📚 Recursos

- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Docs](https://docs.github.com/)
- [Convencional Commits](https://www.conventionalcommits.org/)
- [Protecting Sensitive Data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure)

---

## 🆘 ¿Problemas?

Si algo sale mal:

1. **NO** entres en pánico
2. **NO** borres todo y empieces de nuevo
3. Lee el mensaje de error
4. Busca en Google el error exacto
5. Pregunta en GitHub Discussions o Stack Overflow

**Recuerda**: Git guarda TODO el historial. Es casi imposible perder datos permanentemente.

---

¡Tu código ahora está en GitHub! 🎉
