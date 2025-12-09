# Instrucciones Detalladas para Ejecutar y Probar la API REST

---

## 1. Prerequisitos

Asegurarse de tener instalado:

- **Python 3.8+**: [Descargar Python](https://www.python.org/downloads/)
- **MySQL Server**: [Descargar MySQL](https://dev.mysql.com/downloads/mysql/)
- **Git**: [Descargar Git](https://git-scm.com/downloads)
- **Postman** para probar los endpoints

---

## 2. Clonar el Repositorio

```bash
git clone https://github.com/HolmanSegura/prueba-oblicua.git
cd prueba-oblicua/Api_rest
```

---

## 3. Crear Base de Datos

Ejecutar el archivo SQL para crear las tablas y triggers.

### Con MySQL Workbench:

1. Abre MySQL Workbench.
2. Conéctate a tu servidor MySQL (localhost:3306).
3. Ve a **File** → **Open SQL Script**.
4. Selecciona `../Modelado_base_de_datos/crear_tablas.sql`.
5. Haz clic en **Execute** o presiona `Ctrl+Shift+Enter`.

---

## 4. Configurar Variables de Entorno

Crea o edita el archivo `.env` en la carpeta `Api_rest/`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contrasena_mysql
DB_NAME=tienda_prueba
JWT_SECRET=tu_clave_secreta_segura
JWT_ALGORITHM=HS256
```

---

## 5. Instalar Dependencias

### En Windows (Git Bash):

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```
---

## 6. Levantar el Servidor

```bash
python app.py
```

Deberás ver `Running on http://127.0.0.1:5000`

---

## 7. Probar los Endpoints

### 1. GET /ping (Test de Conexión)

**Método:** GET  
**URL:** `http://localhost:5000/ping`

**Respuesta esperada (200 - OK):**
```json
{
  "message": "API en línea"
}
```

---

### 2. POST /api/login (Autenticación)

**Método:** POST  
**URL:** `http://localhost:5000/api/login`  
**Content-Type:** `application/json`

**JSON de entrada:**
```json
{
  "email": "ana@example.com",
  "password": "ana123"
}
```

**Respuesta esperada (200 - Éxito):**
```json
{
  "exito": true,
  "mensaje": "Login exitoso",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "nombre": "Ana",
    "apellido": "Martínez",
    "email": "ana@example.com"
    "usuario_id": 1,
  }
}
```
---

### 3. GET /api/productos (Listar Productos)

**Método:** GET  
**URL:** `http://localhost:5000/api/productos`

**Respuesta esperada (200 - OK):**
```json
[
  {
    "producto_id": 1,
    "nombre": "Laptop",
    "precio": 800.00,
    "cantidad_disponible": 5,
    "estado": "activado"
  },
  {
    "producto_id": 2,
    "nombre": "Mouse",
    "precio": 25.00,
    "cantidad_disponible": 50,
    "estado": "activado"
  }
]
```

---

### 4. POST /api/orden (Crear Orden)

**Método:** POST  
**URL:** `http://localhost:5000/api/orden`  
**Content-Type:** `application/json`

**JSON de entrada:**
```json
{
  "usuario_id": 1,
  "items": [
    {
      "producto_id": 1,
      "cantidad": 2
    },
    {
      "producto_id": 2,
      "cantidad": 3
    }
  ]
}
```

**Respuesta esperada (201 - Creado):**
```json
{
  "orden_id": 1,
  "total": 1675.00,
  "usuario_id": 1
}
```


