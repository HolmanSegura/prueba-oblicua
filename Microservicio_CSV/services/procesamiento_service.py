import csv
import io

from flask import request, jsonify
from db.base_datos import conexion_bd


def _respuesta_csv(success, insertados, fallidos, errores, status):
    """
    Construye la respuesta estándar del microservicio CSV.
    """
    cuerpo = {
        "success": success,
        "insertados": insertados,
        "fallidos": fallidos,
        "errores": errores,
    }
    return jsonify(cuerpo), status


def procesar_productos_csv():
    """
    Procesa un archivo CSV con productos y los inserta en la base de datos.
    Valida cabeceras, tipos de datos y reglas de negocio.
    """
    # 1. Validar que venga el archivo
    if "file" not in request.files:
        return _respuesta_csv(
            success=False,
            insertados=0,
            fallidos=0,
            errores=["No se envió ningún archivo en el campo 'file'"],
            status=400,
        )

    file = request.files["file"]

    if file.filename == "":
        return _respuesta_csv(
            success=False,
            insertados=0,
            fallidos=0,
            errores=["El nombre de archivo está vacío"],
            status=400,
        )

    try:
        # 2. Leer CSV en memoria (UTF-8)
        text_wrapper = io.TextIOWrapper(file.stream, encoding="utf-8")
        reader = csv.DictReader(text_wrapper)

        # Validar cabeceras esperadas
        columnas_esperadas = {"nombre", "precio", "cantidad_disponible", "estado"}
        if set(reader.fieldnames or []) != columnas_esperadas:
            return _respuesta_csv(
                success=False,
                insertados=0,
                fallidos=0,
                errores=[
                    (
                        "Cabeceras inválidas. Se esperaban "
                        f"{columnas_esperadas} y se encontraron {reader.fieldnames}"
                    )
                ],
                status=400,
            )

        insertados = 0
        fallidos = 0
        errores: list[str] = []

        conn = conexion_bd()
        cursor = conn.cursor()

        insert_sql = """
            INSERT INTO producto (nombre, precio, cantidad_disponible, estado)
            VALUES (%s, %s, %s, %s)
        """

        # 3. Recorrer filas del CSV
        fila_num = 1  # incluye encabezado
        for row in reader:
            fila_num += 1  # primera fila de datos será 2

            nombre = (row.get("nombre") or "").strip()
            precio_str = (row.get("precio") or "").strip()
            cantidad_str = (row.get("cantidad_disponible") or "").strip()
            estado = (row.get("estado") or "").strip().lower()

            # Validaciones básicas
            if not nombre:
                fallidos += 1
                errores.append(f"Fila {fila_num}: nombre es obligatorio")
                continue

            try:
                precio = float(precio_str)
                if precio <= 0:
                    raise ValueError()
            except Exception:
                fallidos += 1
                errores.append(
                    f"Fila {fila_num}: precio inválido ('{precio_str}')"
                )
                continue

            try:
                cantidad = int(cantidad_str)
                if cantidad < 0:
                    raise ValueError()
            except Exception:
                fallidos += 1
                errores.append(
                    (
                        f"Fila {fila_num}: cantidad_disponible inválida "
                        f"('{cantidad_str}')"
                    )
                )
                continue

            if estado not in ("activado", "desactivado"):
                fallidos += 1
                errores.append(
                    (
                        f"Fila {fila_num}: estado inválido ('{estado}'), "
                        "debe ser 'activado' o 'desactivado'"
                    )
                )
                continue

            # 4. Intentar insertar en BD
            try:
                cursor.execute(insert_sql, (nombre, precio, cantidad, estado))
                insertados += 1
            except Exception as e:
                fallidos += 1
                errores.append(
                    f"Fila {fila_num}: error al insertar en BD: {str(e)}"
                )

        conn.commit()
        cursor.close()
        conn.close()

        return _respuesta_csv(
            success=True,
            insertados=insertados,
            fallidos=fallidos,
            errores=errores,
            status=200,
        )

    except Exception as e:
        return _respuesta_csv(
            success=False,
            insertados=0,
            fallidos=0,
            errores=[f"Error general procesando el archivo: {str(e)}"],
            status=500,
        )
