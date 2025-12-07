from flask import request, jsonify
from base_datos import conexion_bd

def crear_orden():
    datos = request.get_json()

    if not datos or 'usuario_id' not in datos or 'items' not in datos:
        return jsonify({'error': 'usuario_id e items son obligatorios'}), 400

    usuario_id = datos['usuario_id']
    items = datos['items']

    if not isinstance(items, list) or len(items) == 0:
        return jsonify({'error': 'items debe ser una lista con al menos un producto'}), 400

    try:
        conn = conexion_bd()
        cursor = conn.cursor(dictionary=True)

        conn.start_transaction()
	
        producto_ids = [item['producto_id'] for item in items]

        formato_in = ','.join(['%s'] * len(producto_ids))
        query_productos = f"""
            SELECT producto_id, estado, cantidad_disponible
            FROM producto
            WHERE producto_id IN ({formato_in})
        """
        cursor.execute(query_productos, producto_ids)
        productos_db = cursor.fetchall()
        productos_dic = {producto['producto_id']: producto for producto in productos_db}

        for item in items:
            id_producto = item.get('producto_id')
            cantidad = item.get('cantidad', 0)

            if id_producto not in productos_dic:
                conn.rollback()
                return jsonify({'error': f'Producto {id_producto} no existe'}), 400

            producto = productos_dic[id_producto]

            if producto['estado'] != 'activado':
                conn.rollback()
                return jsonify({'error': f'Producto {id_producto} no está activo'}), 400

            if cantidad <= 0:
                conn.rollback()
                return jsonify({'error': f'Cantidad inválida para producto {id_producto}'}), 400

            if cantidad > producto['cantidad_disponible']:
                conn.rollback()
                return jsonify({'error': f'Sin stock suficiente para producto {id_producto}'}), 400

        insert_orden = """
            INSERT INTO orden (usuario_id)
            VALUES (%s)
        """
        cursor.execute(insert_orden, (usuario_id,))
        orden_id = cursor.lastrowid

        insert_detalle = """
            INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad)
            VALUES (%s, %s, %s)
        """
        for item in items:
            cursor.execute(
                insert_detalle,
                (orden_id, item['producto_id'], item['cantidad'])
            )

        update_stock = """
            UPDATE producto
            SET cantidad_disponible = cantidad_disponible - %s
            WHERE producto_id = %s
        """
        for item in items:
            cursor.execute(update_stock, (item['cantidad'], item['producto_id']))

        conn.commit()

        cursor.execute("SELECT total FROM orden WHERE orden_id = %s", (orden_id,))
        row = cursor.fetchone()
        total = float(row['total']) if row else 0.0

        return jsonify({
            'orden_id': orden_id,
            'total': total,
            'usuario_id': usuario_id
        }), 201

    except Exception as e:
        try:
            conn.rollback()
        except:
            pass
        return jsonify({'error': str(e)}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
