# Justificación técnica de la base de datos

La base de datos está pensada para manejar usuarios, productos y órdenes, de forma que se puedan hacer consultas como ver las órdenes con su total y los productos más vendidos.

## Se usaron cuatro tablas:

**usuario:** guarda la información de las personas (nombre, apellido, email y password). Tiene una clave primaria numérica para poder relacionarla fácilmente con las órdenes.

**producto:** almacena el catálogo de productos con su nombre, precio, cantidad disponible y un estado (activado/desactivado). El estado permite dejar de usar un producto sin borrarlo, y el tipo numérico decimal del precio evita problemas de precisión al trabajar con dinero.

**orden:** representa cada compra realizada por un usuario. Guarda quién hizo la orden, la fecha y el total. La fecha se llena automáticamente con la fecha actual y el total se inicia en cero y luego se actualiza según los detalles asociados. La relación con usuario impide borrar un usuario que ya tenga órdenes, para no perder historial.

**detalle_orden:** conecta órdenes con productos y define qué se compró exactamente en cada orden (producto, cantidad, precio unitario y subtotal). Aquí se guarda el precio unitario usado en el momento de la compra y también se evita que el mismo producto se repita dos veces en la misma orden.

## Además, se usan triggers para automatizar parte de la lógica:

- Al insertar un detalle de orden, se toma automáticamente el precio actual del producto y se guarda como precio unitario.
- Con ese precio y la cantidad, se calcula de forma automática el subtotal de la línea.
- Después de insertar cada detalle, se vuelve a calcular el total de la orden sumando todos sus subtotales.

Con esto, la base de datos no solo guarda la información, sino que ayuda a mantenerla consistente.
