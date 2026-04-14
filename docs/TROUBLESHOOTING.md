# 🔧 Solución de Problemas Comunes

---

## 🗄️ Problemas con MySQL

### ❌ "Can't connect to MySQL server on 'localhost:3306'"

**Causa:** MySQL no está corriendo

**Solución:**

**Windows:**
```cmd
net start MySQL80
# O busca "Services" en Windows → MySQL80 → Start
```

**macOS:**
```bash
brew services start mysql
# O:
mysql.server start
```

**Linux:**
```bash
sudo systemctl start mysql
# O:
sudo service mysql start
```

**Verificar:**
```bash
mysql -u root -p
# Si pedís password y entras → ✅ Mysqli
```

### ❌ "Access denied for user 'root'@'localhost'"

**Causa:** Contraseña de MySQL incorrecta

**Solución:**

1. Verifica tu password en `.env`:
```env
# Debe ser:
DATABASE_URL=mysql+pymysql://root:AQUI_TU_PASSWORD@localhost:3306/jwt_api_db
```

2. Si olvidaste el password:

**Windows:** Busca "MySQL 8.0 Command Line Client"

**macOS/Linux:**
```bash
sudo mysql

# Dentro de MySQL:
ALTER USER 'root'@'localhost' IDENTIFIED BY 'nueva_password';
FLUSH PRIVILEGES;
exit
```

3. Actualiza `.env` con la nueva contraseña

### ❌ "Field 'created_at' doesn't have a default value"

**Causa:** Tablas viejas sin valores por defecto

**Solución:**

```bash
# Borra y recrea las tablas:
cd backend
python -m app.database

# Selecciona "y" para confirmar
```

O manualmente en MySQL:
```sql
ALTER TABLE users 
MODIFY created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
MODIFY updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE products 
MODIFY created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
MODIFY updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
```

### ❌ "Database does not exist: jwt_api_db"

**Causa:** No creaste la BD

**Solución:**
```bash
mysql -u root -p -e "CREATE DATABASE jwt_api_db;"
```

O desde MySQL Workbench:
```sql
CREATE DATABASE jwt_api_db;
```

---

## 🐍 Problemas Python/Backend

### ❌ "No module named 'app'"

**Causa:** Estás en el directorio equivocado

**Solución:**
```bash
# Asegúrate de estar en backend/
cd jwt-api-project/backend

# Luego:
uvicorn app.main:app --reload
```

### ❌ "ModuleNotFoundError: No module named 'fastapi'"

**Causa:** Entorno virtual no activado o dependencias no instaladas

**Solución:**
```bash
cd backend

# 1. Activar entorno virtual
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 2. Verificar que esté activo (deberías ver (venv) en la terminal)

# 3. Instalar dependencias
pip install -r requirements.txt
```

### ❌ "Address already in use"

**Causa:** El puerto 8000 ya está siendo usado

**Solución:**

**Opción 1: Matar el proceso**
```bash
# Windows (PowerShell):
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

**Opción 2: Usar otro puerto**
```bash
uvicorn app.main:app --reload --port 8001
```

### ❌ "ERROR:  Unauthorized access for user 'root'"

**Causa:** Credenciales MySQL incorrectas

**Solución:** Ver sección "Access denied" arriba

### ❌ "ImportError: cannot import name 'Session' from 'sqlalchemy.orm'"

**Causa:** Versión de SQLAlchemy incompatible

**Solución:**
```bash
pip install sqlalchemy==2.0.23
pip install -r requirements.txt --upgrade
```

### ❌ Backend inicia pero endpoints retornan 500

**Causa:** Error en el código

**Solución:**
1. Mira los logs en la terminal donde corre el backend
2. Verifica que las tablas existan: `python -m app.database`
3. Verifica que MySQL esté corriendo
4. Revisa `.env` para variables faltantes

---

## 🎨 Problemas Node/Frontend

### ❌ "npm: command not found"

**Causa:** Node.js no está instalado

**Solución:**
1. Descarga de https://nodejs.org (versión LTS)
2. Instala y reinicia tu terminal
3. Verifica: `npm --version` (deberías ver: v18+)

### ❌ "Address already in use :4321"

**Causa:** Astro ya está corriendo en ese puerto

**Solución:**

**Opción 1: Matar proceso**
```bash
# Windows (PowerShell):
Get-Process -Id (Get-NetTCPConnection -LocalPort 4321).OwningProcess | Stop-Process

# Mac/Linux:
lsof -ti:4321 | xargs kill -9
```

**Opción 2: Otro puerto en astro.config.mjs**
```javascript
export default defineConfig({
  server: { port: 4322 }
});
```

### ❌ "Cannot find module 'astro'"

**Causa:** npm dependencies no instaladas

**Solución:**
```bash
cd frontend
npm install

# Si aún falla:
rm -rf node_modules package-lock.json
npm install
```

### ❌ Frontend no se conecta al backend (CORS error)

**Síntoma:** `Access to XMLHttpRequest blocked...`

**Causa:** Backend CORS no permite origen del frontend

**Solución:**

1. Edita `backend/.env`:
```env
ALLOWED_ORIGINS=http://localhost:4321,http://localhost:3000
```

2. Reinicia backend:
```bash
# Ctrl + C para detener
# Luego:
uvicorn app.main:app --reload
```

3. Si usas production, actualiza CORS en variables de Railway

---

## 🌐 Problemas de Red/Conectividad

### ❌ "Connection refused" al conectarse a backend

**Causa:** Backend no está corriendo

**Solución:**
```bash
cd backend
uvicorn app.main:app --reload

# Verifica que veas:
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

### ❌ Frontend ve "Cannot load from localhost:8000"

**Causa:** Firewall bloqueando puerto 8000

**Solución:**

**Windows Firewall:**
1. Abre Windows Defender Firewall
2. Click **Allow an app through firewall**
3. Click **Change settings**
4. Click **Allow another app**
5. Busca y agrega `python.exe`
6. OK

**macOS:**
```bash
# Terminal pide permiso automáticamente la primera vez
# Ingresa tu password
```

---

## 🚀 Problemas de Despliegue

### ❌ Build failed en Vercel

**Síntoma:** Vercel log muestra error de build

**Solución:**
1. Verifica que `npm run build` funciona localmente:
```bash
cd frontend
npm run build

# Si funciona: ✅
# Si falla: verifica el error
```

2. En Vercel dashboard:
   - Root Directory: debe ser `frontend/`
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. Redeploy:
   - Proyecto → **Deployments** → botón **Redeploy**

### ❌ Backend no responde en Railway

**Síntoma:** Railway deployment falla

**Solución:**
1. Ve a Railway dashboard
2. Click tu proyecto backend
3. **View Logs**
4. Busca errores específicos
5. Verifica:
   - [ ] DATABASE_URL está configurado
   - [ ] SECRET_KEY no está vacío
   - [ ] Port está correcto ($PORT)

6. Redeploy:
   - Click **Redeploy**

### ❌ CORS error después de deploy

**Síntoma:** Frontend en production no puede llamar backend

**Causa:** ALLOWED_ORIGINS no incluye tu dominio

**Solución:**
1. Railway dashboard → Backend
2. **Variables** 
3. Edita `ALLOWED_ORIGINS`:
```env
ALLOWED_ORIGINS=https://tu-proyecto.vercel.app,https://*.vercel.app
```
4. **Save** (redeploy automático)

### ❌ Login falla después de deploy

**Síntoma:** Login devuelve 401 error

**Causa:** SECRET_KEY diferente entre deploys

**Solución:**
1. Railway → Backend → **Variables**
2. Verifica que `SECRET_KEY` sea el MISMO que usaste localmente
3. Si cambió, genera uno nuevo:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
4. Redeploy

---

## 🆘 Problemas No Listados

### Debug Mode

**Para el Backend:**
```env
# En .env:
DEBUG=True
```

Verás queries SQL en la consola:
```
SELECT * FROM users WHERE email = 'test@ejemplo.com'
```

**Para el Frontend:**
```javascript
// En browser console (F12):
localStorage.getItem('refresh_token')
sessionStorage.getItem('access_token')
```

### Ver Logs en Tiempo Real

**Backend:**
```bash
# La terminal donde corre uvicorn muestra logs automáticamente
```

**Frontend:**
```bash
# Terminal donde corre npm run dev
# Muestra HMR y errors
```

**Railway Production:**
```bash
# Railway dashboard → Backend → View Logs
```

**Vercel Production:**
```bash
# Vercel dashboard → Deployments → View Build Logs
```

---

##  💡 Pasos para Debuggear Cualquier Error

### 1. Lee el error completo
"No copies solo la primera línea, lee TODO el traceback"

### 2. Identifica dónde ocurre
¿En backend? ¿En frontend? ¿En deployment?

### 3. Aísla el problema
¿Es replicable? ¿Ocurre siempre o a veces?

### 4. Busca en Google
Copia el error exacto + tecnología:
```
"Database connection failed" "sqlalchemy" "mysql"
```

### 5. Revisa .env
"El 80% de los problemas son .env mal configurado"

### 6. Reinicia todo
```bash
# Backend:
Ctrl + C
# Borra:
rm -rf .pytest_cache __pycache__
# Reinicia

# Frontend:
Ctrl + C
# Limpia:
npm cache clean --force
# Reinstala:
npm install
npm run dev
```

---

##  📞 Si Nada Funciona

1. Borra `venv/` y `node_modules/`
2. Reinstala todo desde cero:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   
   cd ../frontend
   npm install
   ```

3. Recrea la BD:
   ```sql
   DROP DATABASE jwt_api_db;
   CREATE DATABASE jwt_api_db;
   ```
   ```bash
   python -m app.database
   ```

4. Intenta de nuevo

Si aún falla, revisa [docs/DEVELOPMENT.md](DEVELOPMENT.md) o abre un issue en GitHub.

---

**Buena suerte! 🍀**
