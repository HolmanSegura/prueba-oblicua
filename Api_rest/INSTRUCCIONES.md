# Instrucciones Detalladas para Ejecutar y Probar la API REST

## Resumen

Esta documentación proporciona los pasos completos para configurar, levantar y probar la API REST de la prueba técnica de Oblicua. Incluye configuración de variables de entorno, instalación de dependencias, comandos para iniciar el servidor y ejemplos de pruebas con Postman y cURL.

---

## 1. Prerequisitos

Asegurarse de tener instalado:

- **Python 3.8+**: [Descargar Python](https://www.python.org/downloads/)
- **MySQL Server**: [Descargar MySQL](https://dev.mysql.com/downloads/mysql/)
- **Git**: [Descargar Git](https://git-scm.com/downloads)
- **Postman** o **cURL** para probar los endpoints (opcional para cURL, viene con la mayoría de sistemas)

### Verificar instalaciones

```bash
python --version
mysql --version
git --version
```

---

## 2. Clonar el Repositorio

Abre tu terminal o cmd y ejecuta:

```bash
git clone https://github.com/HolmanSegura/prueba-oblicua.git
cd prueba-oblicua/Api_rest
```

---

## 3. Crear Base de Datos

Antes de levantar la API, ejecutar el archivo SQL para crear las tablas y triggers.

### Con MySQL Workbench:

1. Abre MySQL Workbench.
2. Conéctate a tu servidor MySQL (localhost:3306).
3. Ve a **File** → **Open SQL Script**.
4. Selecciona el archivo `Modelado_base_de_datos/crear_tablas.sql`.
5. Haz clic en **Execute** (el rayo) o presiona `Ctrl+Shift+Enter`.

### Con la línea de comandos (cmd/PowerShell):

```bash
mysql -u root -p < ../Modelado_base_de_datos/crear_tablas.sql
```

Te pedirá la contraseña de MySQL. Después de ejecutarse, verifica que se creó la base de datos `tienda_prueba` con sus tablas.

---

## 4. Configurar Variables de Entorno

En la carpeta `Api_rest/`, edita o crea el archivo `.env` con tus credenciales:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contrasena_mysql
DB_NAME=tienda_prueba
JWT_SECRET=tu_clave_secreta_segura
JWT_ALGORITHM=HS256
```

**Recomendación:** Para una clave segura en JWT_SECRET, usa una cadena larga y aleatoria, por ejemplo:
```
JWT_SECRET=8f4a2b9c3e7d1f6a5e2c9b4d7a1f3e8c
```

---

## 5. Instalar Dependencias

Desde la carpeta `Api_rest/`, crea un entorno virtual e instala las dependencias:

### En Windows (PowerShell o CMD):

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### En macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Verificar instalación:**
```bash
pip list
```

Debes ver: Flask, mysql-connector-python, python-dotenv, PyJWT

---

## 6. Levantar el Servidor

Asegúrate de que el entorno virtual esté activado, luego ejecuta:

```bash
python app.py
```

Deberás ver algo como:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

El servidor estará listo en `http://localhost:5000`.

---

## 7. Probar los Endpoints

Puedes probar los endpoints usando **Postman**, **Insomnia**, o **cURL**.

### 7.1 Endpoint: `/ping` (Test de Conexión)

**Método:** GET  
**URL:** `http://localhost:5000/ping`

#### Con cURL:

```bash
curl -X GET http://localhost:5000/ping
```

**Respuesta Esperada:**
```json
{
  "message": "API en línea"
}
```

---

### 7.2 Endpoint: `/api/login` (Autenticación)

**Método:** POST  
**URL:** `http://localhost:5000/api/login`  
**Content-Type:** `application/json`

#### JSON de Entrada:

```json
{
  "email": "usuario@example.com",
  "password": "contrasena123"
}
```

#### Con cURL:

```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"usuario@example.com\",\"password\":\"contrasena123\"}"
```

#### Respuesta Esperada (200 - Éxito):

```json
{
  "exito": true,
  "mensaje": "Login exitoso",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "usuario_id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "usuario@example.com",
    "password": "contrasena123"
  }
}
```

#### Respuesta de Error (401 - Credenciales Inválidas):

```json
{
  "exito": false,
  "mensaje": "Credenciales inválidas",
  "token": null
}
```

---

### 7.3 Endpoint: `/api/productos` (Listar Productos)

**Método:** GET  
**URL:** `http://localhost:5000/api/productos`

#### Con cURL:

```bash
curl -X GET http://localhost:5000/api/productos
```

#### Respuesta Esperada (200):

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

### 7.4 Endpoint: `/api/orden` (Crear Orden)

**Método:** POST  
**URL:** `http://localhost:5000/api/orden`  
**Content-Type:** `application/json`

#### JSON de Entrada:

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

#### Con cURL:

```bash
curl -X POST http://localhost:5000/api/orden \
  -H "Content-Type: application/json" \
  -d "{\"usuario_id\":1,\"items\":[{\"producto_id\":1,\"cantidad\":2},{\"producto_id\":2,\"cantidad\":3}]}"
```

#### Respuesta Esperada (201 - Creado):

```json
{
  "orden_id": 10,
  "total": 175.00,
  "usuario_id": 1
}
```

#### Respuesta de Error (400 - Sin Stock):

```json
{
  "error": "Sin stock suficiente para producto 1"
}
```

---

## 8. Usar Postman para Pruebas Completas

### Importar Colección (Opcional):

1. Abre Postman.
2. Click en **File** → **New** → **Request**.
3. Ingresa los datos de cada endpoint como se muestra arriba.
4. Guarda las solicitudes en una colección para reutilizarlas.

### Flujo de Prueba Recomendado:

1. Prueba `/ping` para verificar conectividad.
2. Prueba `/api/login` con credenciales válidas e inválidas.
3. Prueba `/api/productos` para listar todos los productos.
4. Prueba `/api/orden` con un usuario y items válidos.
5. Intenta crear una orden con cantidad mayor al stock disponible (debe fallar).

---

## 9. Detener el Servidor

En la terminal donde levantaste el servidor, presiona:

```
Ctrl + C
```

---

## 10. Solucionar Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solución:**
- Verifica que el entorno virtual esté activado.
- Ejecuta `pip install -r requirements.txt` nuevamente.

### Error: "Can't connect to MySQL server"

**Solución:**
- Verifica que MySQL esté corriendo.
- Comprueba las credenciales en `.env` (usuario, contraseña, host, puerto).
- Asegúrate de que la base de datos `tienda_prueba` exista.

### Error: "JWT Secret not found"

**Solución:**
- Verifica que `JWT_SECRET` esté definido en `.env`.

### Error de Transacción en Ordenes

**Solución:**
- Verifica que los `producto_id` sean válidos.
- Comprueba que haya stock disponible para los productos.
- Verifica que el `usuario_id` exista en la BD.

---

## 11. Estructura del Proyecto

```
Api_rest/
├─ app.py                       # Aplicación Flask principal
├─ config.py                    # Configuración centralizada
├─ db/
│  └─ base_datos.py             # Conexión a MySQL
├─ routes/
│  ├─ auth_routes.py            # Rutas de autenticación
│  ├─ productos_routes.py       # Rutas de productos
│  └─ ordenes_routes.py         # Rutas de órdenes
├─ services/
│  ├─ auth_service.py           # Lógica de login y JWT
│  ├─ productos_service.py      # Lógica de productos
│  └─ ordenes_service.py        # Lógica de órdenes
├─ utils/
│  └─ jwt_token.py              # Generación de tokens
├─ requirements.txt             # Dependencias Python
├─ .env                         # Variables de entorno (NO subir al repo)
├─ .env.example                 # Ejemplo de .env
├─ .gitignore                   # Archivos a ignorar en Git
└─ INSTRUCCIONES.md             # Este archivo
```

---

## 12. Notas Finales

- Todos los endpoints retornan JSON.
- Los errores se devuelven con códigos HTTP estándar (400, 401, 500).
- El token JWT tiene expiración de 1 hora.
- Las transacciones en la creación de órdenes garantizan consistencia en la BD.
- Los triggers calculan automáticamente el total de cada orden.

---

**Última actualización:** 8 de diciembre de 2025  
**Autor:** Equipo de Desarrollo  
**Versión:** 1.0
