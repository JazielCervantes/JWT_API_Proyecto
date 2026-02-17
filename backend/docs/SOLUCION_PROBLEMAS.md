# 🔧 Solución de Problemas Comunes

Esta guía contiene soluciones a los errores más comunes al usar el proyecto.

---

## 🗄️ Problemas con MySQL

### ❌ Error: "Field 'created_at' doesn't have a default value"

**Descripción**: Al intentar insertar datos manualmente en MySQL Workbench.

**Causa**: MySQL está en modo estricto y necesita valores explícitos para los campos timestamp.

**Solución 1 - Especificar timestamps en el INSERT**:
```sql
INSERT INTO products (name, description, price, stock, category, brand, sku, is_active, created_at, updated_at) 
VALUES
    ('Laptop Dell XPS 15', 'Descripción...', 1299.99, 10, 'Electrónica', 'Dell', 'DELL-XPS15-001', TRUE, NOW(), NOW());
```

**Solución 2 - Recrear las tablas**:
Si acabas de crear las tablas, elimínalas y recréalas con los modelos actualizados:
```bash
# En Python
python -m app.database
```

Las tablas ahora tendrán `DEFAULT CURRENT_TIMESTAMP` a nivel de MySQL.

**Solución 3 - Modificar tabla existente**:
```sql
ALTER TABLE products 
MODIFY created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
MODIFY updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE users 
MODIFY created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
MODIFY updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
```

---

### ❌ Error: "Can't connect to MySQL server"

**Causa**: MySQL no está ejecutándose.

**Solución**:

**Windows**:
```cmd
net start MySQL80
```

**macOS**:
```bash
brew services start mysql
# O
mysql.server start
```

**Linux**:
```bash
sudo systemctl start mysql
# O
sudo service mysql start
```

**Verificar que esté corriendo**:
```bash
mysql -u root -p -e "SELECT 1"
```

---

### ❌ Error: "Access denied for user 'root'@'localhost'"

**Causa**: Credenciales incorrectas en `.env`.

**Solución**:

1. Verifica tu contraseña de MySQL:
```bash
mysql -u root -p
# Ingresa tu contraseña
```

2. Actualiza `.env`:
```env
DATABASE_URL=mysql+pymysql://root:TU_PASSWORD_REAL@localhost:3306/jwt_api_db
```

3. Si olvidaste la contraseña de root, reinicia MySQL:

**Windows**: Busca "MySQL 8.0 Command Line Client"

**macOS/Linux**:
```bash
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'nueva_password';
FLUSH PRIVILEGES;
```

---

### ❌ Error: "Unknown database 'jwt_api_db'"

**Causa**: La base de datos no existe.

**Solución**:
```sql
CREATE DATABASE jwt_api_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

O desde terminal:
```bash
mysql -u root -p -e "CREATE DATABASE jwt_api_db;"
```

---

## 🐍 Problemas con Python

### ❌ Error: "No module named 'app'"

**Causa**: Ejecutando desde el directorio incorrecto.

**Solución**:
```bash
# Asegúrate de estar en backend/
cd backend
uvicorn app.main:app --reload
```

---

### ❌ Error: "No module named 'fastapi'"

**Causa**: Dependencias no instaladas o entorno virtual no activado.

**Solución**:
```bash
# 1. Activa el entorno virtual
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 2. Verifica que esté activado (deberías ver (venv) en el prompt)

# 3. Instala dependencias
pip install -r requirements.txt
```

---

### ❌ Error: "python-cors==1.0.0 not found"

**Causa**: Versión antigua de requirements.txt.

**Solución**: Descarga la versión actualizada del proyecto. El paquete `python-cors` no existe y fue removido.

---

### ❌ Error: "ModuleNotFoundError: No module named 'pymysql'"

**Causa**: PyMySQL no instalado.

**Solución**:
```bash
pip install pymysql cryptography
```

---

## 🔐 Problemas de Autenticación

### ❌ Error 401: "Token inválido o expirado"

**Causa**: El access token expiró (duran 30 minutos).

**Solución**: Usa el refresh token para obtener uno nuevo.

**En Swagger**:
1. Ve a `/api/auth/refresh`
2. Pega tu refresh_token
3. Copia el nuevo access_token
4. Click en "Authorize" y pégalo

**Con cURL**:
```bash
curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "TU_REFRESH_TOKEN"}'
```

---

### ❌ Error 403: "Se requieren permisos de administrador"

**Causa**: Intentas acceder a un endpoint de admin con usuario normal.

**Solución**: 
- Usa las credenciales de admin: `admin` / `admin123`
- O pide a un admin que cambie tu rol:

```sql
UPDATE users SET role = 'admin' WHERE username = 'tu_usuario';
```

---

### ❌ Error: "Credenciales incorrectas" (al hacer login)

**Solución**:

1. **Verifica que el usuario exista**:
```sql
SELECT username, email FROM users WHERE username = 'tu_usuario';
```

2. **Si olvidaste la contraseña, resetéala**:
```python
# En Python
from app.utils.security import get_password_hash
from app.database import get_db
from app.models.user import User

db = next(get_db())
user = db.query(User).filter(User.username == "tu_usuario").first()
user.hashed_password = get_password_hash("nueva_password")
db.commit()
```

3. **O usa el admin por defecto**:
- Username: `admin`
- Password: `admin123`

---

## 🚀 Problemas al Iniciar el Servidor

### ❌ Error: "Address already in use"

**Causa**: El puerto 8000 ya está en uso.

**Solución 1 - Matar el proceso**:

**Windows**:
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**macOS/Linux**:
```bash
lsof -i :8000
kill -9 <PID>
```

**Solución 2 - Usar otro puerto**:
```bash
uvicorn app.main:app --reload --port 8001
```

---

### ❌ Error: "Unable to import 'app.main'"

**Causa**: Estructura de carpetas incorrecta o falta `__init__.py`.

**Solución**:

1. Verifica la estructura:
```
backend/
├── app/
│   ├── __init__.py  ← Debe existir
│   ├── main.py
│   └── ...
```

2. Asegúrate de que `app/__init__.py` existe (puede estar vacío).

---

## 📊 Problemas con Swagger UI

### ❌ Swagger muestra errores al cargar

**Causa**: Error en el código Python o servidor no está corriendo.

**Solución**:

1. Verifica que el servidor esté corriendo sin errores
2. Revisa la consola por mensajes de error
3. Accede a http://localhost:8000/docs (no /doc ni /swagger)

---

### ❌ "Authorize" no funciona en Swagger

**Síntomas**: Después de autorizar, los endpoints siguen dando 401.

**Solución**:

1. Asegúrate de incluir "Bearer " antes del token:
   - ✅ Correcto: `Bearer eyJhbGc...`
   - ❌ Incorrecto: `eyJhbGc...`

2. Verifica que el token no haya expirado (dura 30 min).

3. Haz login de nuevo si es necesario.

---

## 💾 Problemas con la Base de Datos

### ❌ Tablas no se crean correctamente

**Solución**:

1. Elimina las tablas existentes:
```sql
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;
```

2. Recrea las tablas:
```bash
cd backend
python -m app.database
```

3. Verifica que se crearon:
```sql
SHOW TABLES;
DESCRIBE users;
DESCRIBE products;
```

---

### ❌ Datos duplicados o errores de UNIQUE constraint

**Causa**: Intentas insertar un email, username o SKU que ya existe.

**Solución**:

**Ver qué existe**:
```sql
SELECT username, email FROM users;
SELECT sku FROM products;
```

**Eliminar duplicado**:
```sql
DELETE FROM users WHERE username = 'usuario_duplicado';
```

**O actualizar**:
```sql
UPDATE users SET username = 'nuevo_username' WHERE id = 5;
```

---

## 🐛 Problemas Generales

### ❌ Variables de entorno no se cargan

**Causa**: Archivo `.env` en ubicación incorrecta o mal formateado.

**Solución**:

1. Verifica la ubicación:
```
backend/
├── .env          ← Debe estar aquí
├── app/
└── ...
```

2. Verifica el formato (sin espacios alrededor del =):
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/jwt_api_db
SECRET_KEY=tu_clave_secreta
```

3. Reinicia el servidor después de editar `.env`.

---

### ❌ Slow queries / Rendimiento lento

**Solución**:

1. **Agregar índices**:
```sql
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_price ON products(price);
```

2. **Limitar resultados**:
```
GET /api/products?limit=10
```

3. **Usar paginación**:
```
GET /api/products?skip=0&limit=20
```

---

## 📝 Tips de Debugging

### Ver queries SQL en consola

En `.env`:
```env
DEBUG=True
```

Esto mostrará todas las queries SQL en la consola.

---

### Ver logs detallados

```bash
uvicorn app.main:app --reload --log-level debug
```

---

### Probar conexión a MySQL

```bash
mysql -u root -p -e "USE jwt_api_db; SELECT COUNT(*) FROM users;"
```

---

### Verificar que el token es válido

Ve a https://jwt.io/ y pega tu token para ver su contenido.

---

## 🆘 Si Nada Funciona

1. **Limpia todo y empieza de nuevo**:

```bash
# Eliminar entorno virtual
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Recrear
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

2. **Elimina y recrea la base de datos**:

```sql
DROP DATABASE IF EXISTS jwt_api_db;
CREATE DATABASE jwt_api_db;
```

```bash
python -m app.database
```

3. **Verifica versiones**:

```bash
python --version  # Debe ser 3.10+
mysql --version   # Debe ser 8.0+
pip --version
```

---

## 📞 Recursos Adicionales

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **MySQL Docs**: https://dev.mysql.com/doc/
- **Python Docs**: https://docs.python.org/3/
- **JWT Debugger**: https://jwt.io/

---

## ✅ Checklist de Diagnóstico

Cuando algo falla, verifica:

- [ ] ¿MySQL está corriendo?
- [ ] ¿La base de datos jwt_api_db existe?
- [ ] ¿El entorno virtual está activado?
- [ ] ¿Las dependencias están instaladas?
- [ ] ¿El archivo .env existe y está configurado?
- [ ] ¿Estás en el directorio backend/?
- [ ] ¿El servidor está corriendo sin errores en consola?
- [ ] ¿El token no ha expirado?
- [ ] ¿Tienes los permisos necesarios?

---

**Última actualización**: Febrero 2026  
**Si encuentras otros errores**, revisa los logs en la consola y busca el error específico.
