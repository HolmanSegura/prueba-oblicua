
-- USA LA BASE DE DATOS
USE tienda_prueba;

-- SELECT 1: Obtener todas las órdenes con su total calculado
SELECT o.*, concat(u.nombre, " ", u.apellido) usuario 
FROM orden o JOIN usuario u ON u.usuario_id = o.usuario_id;

-- SELECT 2: Obtener los 5 productos más vendidos
SELECT p.producto_id, p.nombre, SUM(d.orden_cantidad) AS cantidad_vendida
FROM detalle_orden d JOIN producto p ON p.producto_id = d.producto_id
GROUP BY p.producto_id ORDER BY cantidad_vendida DESC LIMIT 5;

-- SELECT 3: Obtener los usuarios que no han realizado ninguna orden
SELECT u.* FROM usuario u LEFT JOIN orden o ON o.usuario_id = u.usuario_id
WHERE o.orden_id IS NULL;

-- SELECT 4: Buscar productos por texto
SELECT * FROM producto WHERE nombre LIKE CONCAT('%Mo%');
