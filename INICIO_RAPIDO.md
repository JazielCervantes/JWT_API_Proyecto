# 🚀 Inicio Rápido

## ⚡ Configuración en 5 minutos

### 1. Requisitos Previos

- Python 3.10+
- MySQL 8.0+
- pip (gestor de paquetes de Python)

### 2. Instalar MySQL

#### Windows
1. Descarga MySQL desde https://dev.mysql.com/downloads/installer/
2. Instala MySQL Workbench y MySQL Server
3. Durante instalación, configura password para root

#### macOS
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

### 3. Crear Base de Datos

Abre MySQL Workbench o terminal MySQL:

```sql
CREATE DATABASE jwt_api_db;
```

O desde terminal:
```bash
mysql -u root -p -e "CREATE DATABASE jwt_api_db;"
```

### 4. Configurar el Proyecto

```bash
# 1. Clonar o descargar el proyecto
cd jwt-api-project/backend

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Copiar archivo de configuración
cp .env.example .env

# 6. Editar .env con tus credenciales
# Abre .env y configura:
# DATABASE_URL=mysql+pymysql://root:tu_password@localhost:3306/jwt_api_db
```

### 5. Generar Secret Key Segura

```bash
# Genera una clave segura
python -c "import secrets; print(secrets.token_hex(32))"

# Copia el resultado y pégalo en .env como SECRET_KEY
```

### 6. Inicializar Base de Datos

```bash
# Crear todas las tablas
python -m app.database
```

Deberías ver:
```
🔧 Creando tablas en la base de datos...
✅ Base de datos inicializada correctamente
```

### 7. Iniciar el Servidor

```bash
uvicorn app.main:app --reload
```

Verás:
```
🚀 Iniciando aplicación...
📦 Inicializando base de datos...
👤 Verificando usuario administrador...
✅ Usuario admin creado: admin
✅ Aplicación iniciada correctamente
📖 Documentación disponible en: http://localhost:8000/docs
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 8. Probar la API

Abre tu navegador en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 9. Primer Login

1. En Swagger, ve a `/api/auth/login`
2. Click en "Try it out"
3. Ingresa:
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
4. Click "Execute"
5. Copia el `access_token`
6. Click en "Authorize" 🔒
7. Pega: `Bearer <tu_token>`
8. ¡Listo! Ahora puedes probar todos los endpoints

---

## 🐛 Troubleshooting

### Error: "Can't connect to MySQL server"

**Solución:**
```bash
# Verifica que MySQL esté corriendo
# Windows:
net start MySQL80

# macOS:
brew services start mysql

# Linux:
sudo systemctl start mysql
```

### Error: "Access denied for user"

**Solución:** Verifica credenciales en `.env`:
```
DATABASE_URL=mysql+pymysql://TU_USUARIO:TU_PASSWORD@localhost:3306/jwt_api_db
```

### Error: "No module named 'app'"

**Solución:** Asegúrate de estar en el directorio correcto:
```bash
cd backend
python -m app.main
```

### Error: "ModuleNotFoundError: No module named 'fastapi'"

**Solución:** Activa el entorno virtual:
```bash
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Luego instala dependencias:
pip install -r requirements.txt
```

---

## 📝 Comandos Útiles

```bash
# Ver tablas en MySQL
mysql -u root -p jwt_api_db -e "SHOW TABLES;"

# Ver usuarios en la base de datos
mysql -u root -p jwt_api_db -e "SELECT * FROM users;"

# Limpiar base de datos (CUIDADO: borra todos los datos)
python -c "from app.database import Base, engine; Base.metadata.drop_all(engine)"

# Recrear tablas
python -m app.database

# Ver logs detallados
uvicorn app.main:app --reload --log-level debug
```

---

## ✅ Checklist de Verificación

- [ ] MySQL instalado y corriendo
- [ ] Base de datos `jwt_api_db` creada
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas
- [ ] Archivo `.env` configurado correctamente
- [ ] Tablas creadas en la base de datos
- [ ] Servidor corriendo en http://localhost:8000
- [ ] Swagger UI accesible
- [ ] Login exitoso con admin/admin123

---

## 🎯 Próximos Pasos

1. **Cambia las credenciales del admin**
   ```python
   # En .env
   ADMIN_PASSWORD=tu_nueva_contraseña_segura
   ```

2. **Prueba crear un usuario normal**
   - Usa `/api/auth/register` en Swagger

3. **Explora los endpoints**
   - Productos: CRUD completo
   - Usuarios: Gestión de perfiles
   - Filtros y paginación

4. **Lee la documentación**
   - `docs/GUIA_DESARROLLADORES.md`
   - `docs/EJEMPLOS_USO.md`

5. **Revisa los scripts SQL**
   - `docs/SQL_SCRIPTS.sql`

---

## 💡 Tips

- Usa Swagger UI para experimentar
- Lee los docstrings en el código
- Revisa los ejemplos en `docs/EJEMPLOS_USO.md`
- Los logs en terminal te ayudan a debuggear
- En desarrollo, DEBUG=True muestra queries SQL

---

## 🆘 ¿Necesitas Ayuda?

1. Revisa los logs en la terminal
2. Consulta `docs/GUIA_DESARROLLADORES.md`
3. Busca el error en Google
4. Revisa que todas las dependencias estén instaladas
5. Verifica que MySQL esté corriendo

---

¡Listo! 🎉 Ahora tienes una API REST profesional funcionando.
