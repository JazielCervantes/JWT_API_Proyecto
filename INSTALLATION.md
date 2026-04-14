# 📖 Guía de Instalación - Setup Completo

**⏱️ Tiempo estimado: 10 minutos**

---

## 📋 Requisitos Previos

Verifica que tengas instalados:

```bash
# Python 3.10+
python --version

# Node.js 18+
node --version
npm --version

# MySQL 8.0+ (o MariaDB)
mysql --version
```

---

## 🗄️ Parte 1: Base de Datos MySQL

### 1. Instalar MySQL

**Windows:**
- Descarga: https://dev.mysql.com/downloads/installer/
- Instala MySQL Server 8.0 y MySQL Workbench
- Configura contraseña para root durante instalación

**macOS:**
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

### 2. Crear Base de Datos

```bash
# Opción 1: Desde terminal
mysql -u root -p -e "CREATE DATABASE jwt_api_db;"

# Opción 2: Desde MySQL Workbench
# Abre MySQL Workbench → File → Open SQL Script → Ejecuta:
# CREATE DATABASE jwt_api_db;
```

### 3. Verificar Conexión

```bash
mysql -u root -p
# Ingresa tu password
# Deberías ver: mysql>

# Verifica la BD creada:
SHOW DATABASES;

# Deberías ver: jwt_api_db

exit
```

---

## 🔧 Parte 2: Backend - FastAPI

### 1. Clonar Proyecto

```bash
# HTTPS
git clone https://github.com/usuario/jwt-api-project.git
cd jwt-api-project

# O SSH
git clone git@github.com:usuario/jwt-api-project.git
cd jwt-api-project
```

### 2. Crear Entorno Virtual

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate

# Verifica que esté activo (deberías ver (venv) en la terminal)
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Espera de 2-5 minutos. Deberías ver: "Successfully installed ..."**

### 4. Configurar Variables de Entorno

```bash
# Copiar template
cp .env.example .env

# Abrir y editar .env
# Windows: start .env (o abre en editor de texto)
# macOS: open .env
# Linux: nano .env
```

**Edita estos valores en `.env`:**

```env
# DATABASE_URL - Reemplaza PASSWORD con tu contraseña de MySQL
DATABASE_URL=mysql+pymysql://root:PASSWORD@localhost:3306/jwt_api_db

# Generar SECRET_KEY segura:
# Windows Command Prompt:
#   python -c "import secrets; print(secrets.token_hex(32))"
# O en PowerShell:
#   python -c "import secrets; print(secrets.token_hex(32))"

SECRET_KEY=aqui_pega_el_resultado_del_comando_anterior

# Resto de configuración (puede quedar igual):
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=True                    # False en producción
ALLOWED_ORIGINS=http://localhost:4321,http://localhost:3000
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123       # CAMBIAR EN PRODUCCIÓN
```

### 5. Inicializar Base de Datos

```bash
# Crea las tablas en MySQL
python -m app.database

# Deberías ver:
# 🔧 Creando tablas...
# ✅ Base de datos inicializada
```

### 6. Iniciar Servidor Backend

```bash
uvicorn app.main:app --reload

# Verás:
# ✅ Aplicación iniciada correctamente
# 📖 Documentación: http://localhost:8000/docs
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend corriendo en:** http://localhost:8000

**NO CIERRES esta terminal. Abre otra para el frontend.**

---

## 🎨 Parte 3: Frontend - Astro

### 1. Abrir Nueva Terminal

```bash
# En el directorio raíz del proyecto
cd frontend
```

### 2. Instalar Dependencias

```bash
npm install

# Espera de 2-5 minutos
```

### 3. Configurar Variables de Entorno

```bash
# Copiar template
cp .env.example .env

# Abrir .env en editor:
# Windows: start .env
# macOS: open .env
# Linux: nano .env
```

**Edita con:**
```env
PUBLIC_API_URL=http://localhost:8000
```

### 4. Iniciar Servidor Frontend

```bash
npm run dev

# Verás:
# 🚀 astro dev server running on http://localhost:4321
```

✅ **Frontend corriendo en:** http://localhost:4321

---

## ✅ Verificación Rápida

###  1. Probar Backend

**Opción A: Swagger UI (Recomendado)**
1. Ve a: http://localhost:8000/docs
2. Click en `/auth/login`
3. Click en "Try it out"
4. Ingresa:
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
5. Click "Execute"
6. Deberías ver status 200 y tokens en respuesta

**Opción B: cURL**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

### 2. Probar Frontend

1. Abre: http://localhost:4321
2. Deberías ver:
   - Logo en esquina superior
   - Página de inicio con links
   - Botones de "Registrarse" e "Iniciar Sesión"

3. Click en "Iniciar Sesión"
4. Ingresa:
   - Usuario: `admin`
   - Contraseña: `admin123`
5. Deberías ver el dashboard con información del usuario

### 3. Probar Integración

- Ir a "Productos" - ¿Se cargan productos?
- Ir a "Perfil" - ¿Muestra tus datos?
- Click "Logout" - ¿Se cierra sesión?

✅ **Si todo funciona, ¡está todo listo!**

---

## 🆘 Problemas Comunes

### ❌ Error: "Can't connect to MySQL server"

**Solución:**
```bash
# Verificar que MySQL esté corriendo

# Windows:
net start MySQL80
# O busca "Services" → MySQL → Start

# macOS:
brew services start mysql

# Linux:
sudo systemctl start mysql
```

### ❌ Error: "Access denied for user 'root'"

**Solución:**
1. Verifica tu password en `.env`
2. Si olvidaste el password:
   - Windows: Busca "MySQL 8.0 Command Line Client"
   - macOS/Linux: `sudo mysql`
   - Ejecuta: `ALTER USER 'root'@'localhost' IDENTIFIED BY 'nueva_password';`

### ❌ Error: "Address already in use"

**Solución:** El puerto ya está ocupado
```bash
# Usa otro puerto:
# Backend:
uvicorn app.main:app --reload --port 8001

# Frontend: Edita astro.config.mjs y cambia puerto
```

### ❌ Error: "No module named 'app'"

**Solución:** Estás en el directorio equivocado
```bash
# Asegúrate de estar en backend/
cd backend
uvicorn app.main:app --reload
```

### ❌ npm ERR! command not found: npm

**Solución:** Node.js no está instalado
- Descarga de: https://nodejs.org/ (LTS)
- Instala y reinicia terminal

Ver [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) para más problemas.

---

## 📊 URLs Después del Setup

| Componente | URL |
|-----------|-----|
| **Frontend** | http://localhost:4321 |
| **Backend API** | http://localhost:8000 |
| **Swagger/Docs** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **MySQL** | localhost:3306 |

---

## 📝 Estructura de Carpetas (Después del Setup)

```
jwt-api-project/
├── backend/
│   ├── .venv/                    ← Tu entorno virtual
│   ├── .env                      ← Tu configuración (NO COMMITS)
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   └── ...
│   └── requirements.txt
│
├── frontend/
│   ├── node_modules/             ← Dependencias (NO COMMITS)
│   ├── .env                      ← Tu configuración (NO COMMITS)
│   ├── src/
│   │   ├── pages/
│   │   ├── lib/
│   │   └── styles/
│   └── package.json
│
└── docs/
    ├── DEVELOPMENT.md
    ├── EXAMPLES.md
    ├── DEPLOYMENT.md
    └── TROUBLESHOOTING.md
```

---

## 🎓 Próximos Pasos

### Entender el Código
📖 Lee [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) para entender:
- Conceptos fundamentales (REST, JWT, Roles)
- Arquitectura del proyecto
- Cómo funciona la autenticación

### Ver Ejemplos
💻 Ve a [docs/EXAMPLES.md](docs/EXAMPLES.md) para:
- Ejemplos de cURL
- Ejemplos de Python
- Ejemplos de JavaScript
- Usar Postman

### Hacer Cambios
✏️ Modifica:
- Modelos en `backend/app/models/`
- Endpoints en `backend/app/routes/`
- Frontend en `frontend/src/pages/`

### Deploy a Producción
🚀 Cuando estés listo: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 💡 Tips Útiles

### Reactivar Entorno Virtual

Si cierras la terminal, para volver a trabajar:

```bash
cd backend

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Detener Servidores

```bash
# En las terminales donde corren frontend/backend:
Ctrl + C

# Luego puedes cerrar las terminales
```

### Recrear Base de Datos

Si algo se daña:
```bash
# En MySQL:
DROP DATABASE jwt_api_db;
CREATE DATABASE jwt_api_db;

# Luego en terminal:
cd backend
python -m app.database
```

### Actualizar Dependencias

```bash
# Backend:
pip install -r requirements.txt --upgrade

# Frontend:
npm update
```

---

## ✅ Checklist Final

- [ ] MySQL instalado y corriendo
- [ ] Base de datos `jwt_api_db` creada
- [ ] Entorno virtual Python activado
- [ ] Backend dependencias instaladas
- [ ] `.env` del backend configurado
- [ ] Backend corriendo en port 8000
- [ ] Frontend dependencias instaladas
- [ ] `.env` del frontend configurado
- [ ] Frontend corriendo en port 4321
- [ ] Puedo hacer login con admin/admin123
- [ ] Vi el dashboard después del login

🎉 **¡Felicidades! Todo está listo.**

---

**¿Necesitas ayuda?** Ver [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
