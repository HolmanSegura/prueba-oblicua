# Instrucciones Detalladas para Ejecutar y Probar el MICROSERVICIO

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
cd prueba-oblicua/microservicio_CSV
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

Crea o edita el archivo `.env` en la carpeta `Microservicio_CSV/`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contrasena_mysql
DB_NAME=tienda_prueba
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

Deberás ver `Running on http://127.0.0.1:5100`

---

## 7. Probar los Endpoints

### 1. GET /ping (Test de Conexión)

**Método:** GET  
**URL:** `http://localhost:5100/ping`

**Respuesta esperada (200 - OK):**
```json
{
  "message": "Microservicio CSV en línea"
}
```

---

### 2. POST /procesar-productos-csv (Procesar archivo CSV para ingreso de productos)

**Método:** POST  
**URL:** `http://localhost:5100/procesar-productos-csv`  
**Content-Type:** `multipart/form-data`

**Body de entrada:**

**Name:** `file`
**Type:** `File`
**File** `selecciona el archivo de ejemplo ejemplo_subida_productos.csv en la carpeta archivo_csv`

**Respuesta esperada (200 - OK):**
```json
{
	"errores": [
		"Fila 2: precio inválido ('')",
		"Fila 5: precio inválido ('')"
	],
	"fallidos": 2,
	"insertados": 8,
	"success": true
}
```

### 3. GET /productos (Listar Productos)

**Método:** GET  
**URL:** `http://localhost:5100/productos`

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
