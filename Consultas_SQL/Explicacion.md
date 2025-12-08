# Explicación de las Consultas SQL

## SELECT 1: Obtener todas las órdenes con su total calculado

Esta consulta une la tabla de órdenes con la de usuarios.
Por cada orden trae todos los campos de la tabla orden y del usuario. Gracias a los triggers, el campo total ya viene calculado en la tabla orden, así que aquí solo se está leyendo la información y no se recalcula nada.
Si no existiera el trigger que actualiza el total, habría que sumar los subtotales desde la tabla detalle orden, agrupar por orden y usuario para obtener el total en cada consulta.

## SELECT 2: Obtener los 5 productos más vendidos

En esta consulta se trabaja sobre el detalle de las órdenes.
Se calcula cuántas unidades se han vendido de cada producto sumando la columna de cantidad y agrupando por producto. Luego se ordena de mayor a menor según esa cantidad y se toma solo el top 5, que corresponde a los productos más vendidos.

## SELECT 3: Obtener los usuarios que no han realizado ninguna orden

Aquí se hace un LEFT JOIN de usuarios con órdenes.
Primero se traen todos los usuarios, tengan o no órdenes y después se filtra para dejar únicamente los casos donde la orden es nula. Esto permite identificar usuarios registrados que todavía no han realizado ninguna compra.

## SELECT 4: Buscar productos por texto

Esta consulta busca productos por nombre usando un patrón de texto.
La condición con LIKE y los símbolos % antes y después del texto indica que se quieren productos cuyo nombre contenga esa cadena en cualquier parte. En el backend, ese texto se recibiría como parámetro y se validaría para evitar problemas de seguridad como SQL Injection.
