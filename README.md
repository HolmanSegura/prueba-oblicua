# Prueba Técnica Oblicua

> Prueba técnica de Oblicua para evaluación de competencias en desarrollo backend, bases de datos y arquitectura de microservicios.

---

## Descripción General

Este proyecto implemeta un sistema que incluye gestión de usuarios, productos y órdenes de compra. La solución está diseñada con una arquitectura de microservicios, utilizando Flask como framework principal y MySQL como base de datos relacional.

## Arquitectura del Proyecto

```
prueba-oblicua/
├── Api_rest/                    # API REST principal
├── Microservicio_CSV/           # Microservicio para carga de CSV
├── Consultas_SQL/               # Consultas SQL
├── Modelado_base_de_datos/      # Scripts y diagramas de BD
├── postman/collections/         # Collection de Postman
└── README.md                    # Este archivo
```

---

## Componentes del Sistema

### 1 [Modelado de Base de Datos](./Modelado_base_de_datos)

**Descripción:** Diseño completo de la base de datos con scripts de creación y documentación técnica.

**Contenido:**
- Script SQL de creación de tablas
- Diagrama Entidad-Relación (ER)
- Justificación técnica del diseño
- Triggers automáticos para cálculos

**Tablas principales:**
- `usuario` - Información de usuarios registrados
- `producto` - Catálogo de productos
- `orden` - Órdenes de compra
- `detalle_orden` - Detalles de cada orden

**[Ver justificación técnica](./Modelado_base_de_datos/justificacion_tecnica_BD.md)**

---

### 2 [Consultas SQL](./Consultas_SQL)

**Descripción:** Colección de consultas SQL.

**Consultas incluidas:**
1. Obtener todas las órdenes con su total calculado
2. Top 5 productos más vendidos
3. Usuarios sin órdenes registradas
4. Búsqueda de productos por texto

**[Ver explicación de consultas](./Consultas_SQL/Explicacion.md)**

---

### 3 [API REST](./Api_rest)

**Puerto:** `5000`  
**Descripción:** API principal que maneja la lógica de negocio del sistema.

**Endpoints principales:**
- `POST /api/login` - Autenticación de usuarios
- `GET /api/productos` - Listar productos disponibles
- `POST /api/orden` - Crear nueva orden de compra

**[Ver documentación detallada](./Api_rest/INSTRUCCIONES.md)**

---

### 4 [Microservicio CSV](./Microservicio_CSV)

**Puerto:** `5100`  
**Descripción:** Microservicio especializado en la carga masiva de productos desde archivos CSV.

**Endpoints principales:**
- `POST /procesar-productos-csv` - Cargar productos desde CSV
- `GET /productos` - Verificar productos cargados

**[Ver documentación detallada](./Microservicio_CSV/INSTRUCCIONES.md)**

---

### 5️ [Postman](./postman)

**Descripción:** Collection de Postman con los endpoints principales del API REST y del microservicio CSV.

**Contenido:**
- Collection de Postman con los endpoints principales del API REST y del microservicio CSV

**[Ver collection](./postman/collections)**

---

## Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| **Backend** | Python 3.8+ |
| **Framework** | Flask |
| **Base de Datos** | MySQL 8.0+ |
| **Autenticación** | JWT (PyJWT) |
| **ORM/Conector** | mysql-connector-python |
| **Variables de Entorno** | python-dotenv |
| **Pruebas** | Postman |

---

## Estructura de Archivos

```
prueba-oblicua/
│
├── Api_rest/
│   ├── app.py                  # Punto de entrada de la API
│   ├── config.py               # Configuración
│   ├── requirements.txt        # Dependencias Python
│   ├── .env                    # Variables de entorno (crear)
│   ├── routes/                 # Endpoints de la API
│   ├── services/               # Lógica de negocio
│   ├── db/                     # Conexión a base de datos
│   └── utils/                  # Utilidades (JWT, etc.)
│
├── Microservicio_CSV/
│   ├── app.py                  # Punto de entrada del microservicio
│   ├── config.py               # Configuración
│   ├── requirements.txt        # Dependencias Python
│   ├── .env                    # Variables de entorno (crear)
│   ├── routes/                 # Endpoints del microservicio
│   ├── services/               # Procesamiento de CSV
│   ├── db/                     # Conexión a base de datos
│   └── archivo_csv/            # Archivos CSV de ejemplo
│
├── Consultas_SQL/
│   ├── consultas.sql           # Consultas SQL de ejemplo
│   └── Explicacion.md          # Documentación de consultas
│
├── Modelado_base_de_datos/
│   ├── crear_tablas.sql        # Script de creación de BD
│   ├── diagrama_ER.png         # Diagrama Entidad-Relación
│   ├── diagrama.mwb            # Archivo MySQL Workbench
│   └── justificacion_tecnica_BD.md  # Documentación técnica
│
├── postman/                    
│   ├── collections             # Collection de Postman
│      ├── Api_rest             # Collection de la API REST
│      └── Microservicio_CSV    # Collection del microservicio CSV
│
├── .gitignore                  # Archivos ignorados por Git
└── README.md                   # Este archivo
```

---

## Licencia

Este proyecto fue desarrollado como parte de una prueba técnica para Oblicua.
