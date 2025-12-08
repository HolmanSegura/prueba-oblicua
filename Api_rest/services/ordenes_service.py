from flask import request, jsonify
from db.base_datos import conexion_bd

def _respuesta_orden_error(mensaje, status=400):
    return jsonify({"error": mensaje}), status


def crear_orden():
    """
    Crea una orden con sus detalles, validando productos, stock y estado,
    usando una transacción para asegurar consistencia.
    """
    datos = request.get_json(silent=True) or {}

    usuario_id = datos.get("usuario_id")
    items = datos.get("items")

    # Validar cuerpo de la petición
    if not usuario_id or items is None:
        return _respuesta_orden_error(
            "usuario_id e items son obligatorios", status=400
        )

    if not isinstance(items, list) or len(items) == 0:
        return _respuesta_orden_error(
            "items debe ser una lista con al menos un producto", status=400
        )

    conn = None
    cursor = None

    try:
        # Conectar y preparar transacción
        conn = conexion_bd()
        cursor = conn.cursor(dictionary=True)
        conn.start_transaction()

        # Traer productos involucrados
        producto_ids = [item["producto_id"] for item in items]
        formato_in = ",".join(["%s"] * len(producto_ids))

        query_productos = f"""
            SELECT producto_id, estado, cantidad_disponible
            FROM producto WHERE producto_id IN ({formato_in})
        """
        cursor.execute(query_productos, producto_ids)
        productos_db = cursor.fetchall()
        productos_dic = {
            producto["producto_id"]: producto for producto in productos_db
        }

        # Validar existencia, estado y stock de cada item
        for item in items:
            id_producto = item.get("producto_id")
            cantidad = item.get("cantidad", 0)

            if id_producto not in productos_dic:
                conn.rollback()
                return _respuesta_orden_error(
                    f"Producto {id_producto} no existe", status=400
                )

            producto = productos_dic[id_producto]

            if producto["estado"] != "activado":
                conn.rollback()
                return _respuesta_orden_error(
                    f"Producto {id_producto} no está activo", status=400
                )

            if cantidad <= 0:
                conn.rollback()
                return _respuesta_orden_error(
                    f"Cantidad inválida para producto {id_producto}", status=400
                )

            if cantidad > producto["cantidad_disponible"]:
                conn.rollback()
                return _respuesta_orden_error(
                    f"Sin stock suficiente para producto {id_producto}", status=400
                )

        # Insertar orden
        insert_orden = "INSERT INTO orden (usuario_id) VALUES (%s)"
        cursor.execute(insert_orden, (usuario_id,))
        orden_id = cursor.lastrowid

        # Insertar detalle_orden
        insert_detalle = """
            INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad)
            VALUES (%s, %s, %s)
        """
        for item in items:
            cursor.execute(
                insert_detalle,
                (orden_id, item["producto_id"], item["cantidad"]),
            )

        # Actualizar stock de productos
        update_stock = """
            UPDATE producto
            SET cantidad_disponible = cantidad_disponible - %s
            WHERE producto_id = %s
        """
        for item in items:
            cursor.execute(
                update_stock,
                (item["cantidad"], item["producto_id"]),
            )

        # Confirmar transacción
        conn.commit()

        # Obtener total de la orden
        cursor.execute(
            "SELECT total FROM orden WHERE orden_id = %s", (orden_id,)
        )
        row = cursor.fetchone()
        total = float(row["total"]) if row else 0.0

        return jsonify(
            {
                "orden_id": orden_id,
                "total": total,
                "usuario_id": usuario_id,
            }
        ), 201

    except Exception as e:
        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass
        return jsonify({"error": str(e)}), 500

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
