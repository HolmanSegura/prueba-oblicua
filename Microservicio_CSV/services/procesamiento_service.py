import csv
import io

from flask import request, jsonify
from db.base_datos import conexion_bd


def _respuesta_csv(exitoso, insertados, fallidos, errores, status):
    """
    Construye la respuesta estándar del microservicio CSV.
    """
    cuerpo = {
        "exitoso": exitoso,
        "insertados": insertados,
        "fallidos": fallidos,
        "errores": errores,
    }
    return jsonify(cuerpo), status


def _insertar_lote_productos(cursor, insert_sql, lote_valido):
    """
    Inserta un lote de productos usando executemany.
    Devuelve la cantidad insertada y un posible mensaje de error (o None).
    """
    if not lote_valido:
        return 0, None

    try:
        cursor.executemany(insert_sql, lote_valido)
        cantidad = len(lote_valido)
        lote_valido.clear()
        return cantidad, None
    except Exception as e:
        # Si falla el lote, lo limpiamos y reportamos el error
        cantidad = len(lote_valido)
        lote_valido.clear()
        return 0, f"Error al insertar lote en BD: {str(e)}"


def procesar_productos_csv():
    """
    Procesa un archivo CSV con productos y los inserta en la base de datos.
    Valida cabeceras, tipos de datos y reglas de negocio.
    Usa inserciones por lote (batch) para mejorar rendimiento.
    """
    # Valida que venga el archivo
    if "file" not in request.files:
        return _respuesta_csv(
            exitoso=False,
            insertados=0,
            fallidos=0,
            errores=["No se envió ningún archivo en el campo 'file'"],
            status=400,
        )

    file = request.files["file"]

    if file.filename == "":
        return _respuesta_csv(
            exitoso=False,
            insertados=0,
            fallidos=0,
            errores=["El nombre de archivo está vacío"],
            status=400,
        )

    conn = None
    cursor = None

    try:
        text_wrapper = io.TextIOWrapper(file.stream, encoding="utf-8")
        reader = csv.DictReader(text_wrapper)

        columnas_esperadas = {"nombre", "precio", "cantidad_disponible", "estado"}
        if set(reader.fieldnames or []) != columnas_esperadas:
            return _respuesta_csv(
                exitoso=False,
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

        BATCH_SIZE = 5
        lote_valido: list[tuple] = []

        fila_num = 1
        for row in reader:
            fila_num += 1

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

            # Acumular en lote
            lote_valido.append((nombre, precio, cantidad, estado))

            # Si se llena el lote, insertarlo
            if len(lote_valido) >= BATCH_SIZE:
                cantidad_insertada, error_lote = _insertar_lote_productos(
                    cursor, insert_sql, lote_valido
                )
                insertados += cantidad_insertada
                if error_lote:
                    fallidos += BATCH_SIZE
                    errores.append(
                        f"{error_lote} (hasta fila {fila_num})"
                    )

        # Insertar el lote restante
        if lote_valido:
            cantidad_insertada, error_lote = _insertar_lote_productos(
                cursor, insert_sql, lote_valido
            )
            insertados += cantidad_insertada
            if error_lote:
                fallidos += len(lote_valido)
                errores.append(error_lote)

        conn.commit()

        return _respuesta_csv(
            exitoso=True,
            insertados=insertados,
            fallidos=fallidos,
            errores=errores,
            status=200,
        )

    except Exception as e:
        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass

        return _respuesta_csv(
            exitoso=False,
            insertados=0,
            fallidos=0,
            errores=[f"Error general procesando el archivo: {str(e)}"],
            status=500,
        )

    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
