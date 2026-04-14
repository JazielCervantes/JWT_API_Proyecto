# Instalación y configuración local

Tiempo estimado: 10-15 minutos dependiendo de si ya tienes MySQL instalado.

---

## Requisitos

Antes de empezar verifica que tienes:

```bash
python --version    # 3.10 o superior
node --version      # 18 o superior
mysql --version     # 8.0 o superior
```

Si te falta alguno, instálalo desde su sitio oficial antes de continuar.

---

## Parte 1: Base de datos MySQL

### Instalar MySQL

**Windows:** Descarga el instalador desde https://dev.mysql.com/downloads/installer/ e instala MySQL Server 8.0. Durante la instalación te pedirá una contraseña para el usuario `root`, anótala.

**macOS:**
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install mysql-server
sudo mysql_secure_installation
```

### Crear la base de datos

```bash
mysql -u root -p
```

Dentro de MySQL:
```sql
CREATE DATABASE jwt_api_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
exit;
```

---

## Parte 2: Backend

### 1. Entorno virtual

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

El prompt debería mostrar `(venv)` al inicio cuando está activo.

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus datos. Los campos que sí o sí debes cambiar son:

```env
# Tu contraseña de MySQL
DATABASE_URL=mysql+pymysql://root:TU_PASSWORD@localhost:3306/jwt_api_db

# Genera una clave segura con este comando:
# python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=pega_aqui_el_resultado

# Para desarrollo local puedes dejarlo en True
DEBUG=True

# Orígenes permitidos para CORS
ALLOWED_ORIGINS=http://localhost:4321,http://localhost:3000
```

El resto de valores en `.env.example` pueden quedarse como están para desarrollo.

### 4. Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

Al arrancar verás en los logs que se crean las tablas y el usuario admin. Puedes verificar en http://localhost:8000/health que responda `{"status":"healthy"}`.

La documentación interactiva está en http://localhost:8000/docs.

---

## Parte 3: Frontend

Abre una nueva terminal (deja el backend corriendo).

### 1. Instalar dependencias

```bash
cd frontend
npm install
```

### 2. Variables de entorno

```bash
cp .env.example .env
```

El archivo `.env` solo necesita una línea:

```env
PUBLIC_API_URL=http://localhost:8000
```

### 3. Iniciar en modo desarrollo

```bash
npm run dev
```

Abre http://localhost:4321. El login inicial es `admin` / `admin123`.

---

## Cargar productos de ejemplo

El proyecto incluye un script para poblar la base de datos con 20 productos de muestra:

```bash
# Desde la raíz del proyecto:
python seed_products.py
```

Toma la configuración de `DATABASE_URL` desde `backend/.env` automáticamente. Si necesitas apuntar a otra base de datos, puedes pasarlo como argumento:

```bash
python seed_products.py "mysql+pymysql://user:pass@host:port/db"
```

---

## Credenciales por defecto

| Campo | Valor |
|---|---|
| Usuario admin | `admin` |
| Contraseña | `admin123` |
| Email | `admin@ejemplo.com` |

**Cambia estos valores antes de cualquier despliegue a producción**, ya sea en las variables de entorno de Railway o directamente en `.env`.

---

## Verificación rápida

Si todo está bien deberías poder:

1. Ver Swagger en http://localhost:8000/docs
2. Hacer login en http://localhost:4321/login con `admin` / `admin123`
3. Ver el dashboard con estadísticas
4. Crear, editar y eliminar productos

Si algo falla, revisa [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).
