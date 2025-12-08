
-- CREAR BASE DE DATOS
CREATE DATABASE IF NOT EXISTS tienda_prueba CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- USA LA BASE DE DATOS
USE tienda_prueba;

-- TABLA 1: usuarios
CREATE TABLE usuario(
    usuario_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLA 2: productos
CREATE TABLE producto(
    producto_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    cantidad_disponible INT NOT NULL DEFAULT 0,
    estado VARCHAR(25) NOT NULL DEFAULT 'desactivado'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLA 3: orden
CREATE TABLE orden(
    orden_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    total DECIMAL(10, 2) NOT NULL DEFAULT 0,
    FOREIGN KEY (usuario_id) REFERENCES usuario(usuario_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLA 4: detalle_orden
CREATE TABLE detalle_orden(
    detalle_orden_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    orden_id INT NOT NULL,
    producto_id INT NOT NULL,
    orden_cantidad INT NOT NULL,
    orden_precio_unitario DECIMAL(10,2) NOT NULL,
    orden_subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (orden_id) REFERENCES orden(orden_id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES producto(producto_id) ON DELETE RESTRICT,
    UNIQUE KEY uq_orden_producto (orden_id, producto_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TRIGGER 1: Asignar precio unitario del producto automáticamente
DELIMITER $$
CREATE TRIGGER asignar_precio_unitario
BEFORE INSERT ON detalle_orden
FOR EACH ROW
BEGIN
    DECLARE precio_actual DECIMAL(10,2);
    
    SELECT precio INTO precio_actual 
    FROM producto 
    WHERE producto_id = NEW.producto_id;
    
    SET NEW.orden_precio_unitario = precio_actual;
END$$
DELIMITER ;

-- TRIGGER 2: Calcular orden_subtotal automáticamente
DELIMITER $$
CREATE TRIGGER calcular_subtotal_detalle
BEFORE INSERT ON detalle_orden
FOR EACH ROW
BEGIN
    SET NEW.orden_subtotal = NEW.orden_cantidad * NEW.orden_precio_unitario;
END$$
DELIMITER ;

-- TRIGGER 3: Actualizar total de orden después de insertar detalle
DELIMITER $$
CREATE TRIGGER actualizar_total_orden
AFTER INSERT ON detalle_orden
FOR EACH ROW
BEGIN
    UPDATE orden 
    SET total = (SELECT SUM(orden_subtotal) FROM detalle_orden WHERE orden_id = NEW.orden_id)
    WHERE orden_id = NEW.orden_id;
END$$
DELIMITER ;

-- INSERT 1: ingreso de usuarios
INSERT INTO usuario (nombre, apellido, email, password) VALUES
('Juan',  'Rodríguez', 'juan@example.com',   'juan123'),
('María', 'García',    'maria@example.com',  'maria123'),
('Carlos','López',     'carlos@example.com', 'carlos123'),
('Ana',   'Martínez',  'ana@example.com',    'ana123'),
('Pedro', 'Fernández', 'pedro@example.com',  'pedro123'),
('Laura', 'Sánchez',   'laura@example.com',  'laura123'),
('Diego', 'Pérez',     'diego@example.com',  'diego123'),
('Sofia', 'Gómez',     'sofia@example.com',  'sofia123');

-- INSERT 2: ingreso de productos
INSERT INTO producto (nombre, precio, cantidad_disponible, estado) VALUES
('Laptop HP 15"', 850.00, 10, 'activado'),
('Mouse Logitech', 25.50, 50, 'activado'),
('Teclado Mecánico', 120.00, 30, 'activado'),
('Monitor LG 24"', 250.00, 15, 'activado'),
('Webcam HD 1080p', 60.00, 40, 'activado'),
('Auriculares Sony', 180.00, 25, 'activado'),
('Cable USB-C', 15.00, 100, 'activado'),
('SSD 500GB', 70.00, 0, 'desactivado'),
('RAM DDR4 16GB', 95.00, 35, 'activado'),
('Adaptador HDMI', 12.50, 60, 'activado');

-- INSERT 3: ingreso de ordenes
-- fecha (si no mandas fecha, MySQL pone la actual)
-- total (se inicializa en 0 por defecto y luego el trigger lo recalcula)
INSERT INTO orden (usuario_id, fecha) VALUES
-- Juan (3 órdenes)
(1, '2025-11-01 10:30:00'),
(1, '2025-11-05 14:15:00'),
(1, '2025-11-10 09:45:00'),
-- María (2 órdenes)
(2, '2025-11-02 11:20:00'),
(2, '2025-11-08 16:40:00'),
-- Carlos (1 orden)
(3, '2025-11-03 13:50:00'),
-- Ana (4 órdenes)
(4, '2025-11-04 15:30:00'),
(4, '2025-11-06 10:15:00'),
(4, '2025-11-09 12:00:00'),
(4, '2025-11-12 14:25:00'),
-- Pedro (2 órdenes)
(5, '2025-11-07 08:45:00'),
(5, '2025-11-11 17:10:00');

-- Orden 1 (Juan)
INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad) VALUES
(1, 1, 1),    -- Laptop HP 15"
(1, 2, 1),    -- Mouse Logitech
(1, 10, 2);   -- Adaptador HDMI

-- Orden 2 (Juan)
INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad) VALUES
(2, 4, 1),    -- Monitor LG 24"
(2, 7, 1);    -- Cable USB-C

-- Orden 3 (Juan)
INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad) VALUES
(3, 6, 1);    -- Auriculares Sony

-- Orden 4 (María)
INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad) VALUES
(4, 3, 3);    -- 3x Teclado Mecánico

-- Orden 5 (María)
INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad) VALUES
(5, 5, 1),    -- Webcam HD
(5, 2, 1),    -- Mouse Logitech
(5, 10, 2);   -- Adaptador HDMI

-- Orden 6 (Carlos)
INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad) VALUES
(6, 9, 4),    -- RAM DDR4 16GB
(6, 10, 4);   -- Adaptador HDMI

-- Orden 7 (Ana)
INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad) VALUES
(7, 4, 1),    -- Monitor LG 24"
(7, 2, 1);    -- Mouse Logitech

-- Orden 8 (Ana)
INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad) VALUES
(8, 1, 1);    -- Laptop HP 15"

-- Orden 9 (Ana)
INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad) VALUES
(9, 2, 3),    -- 3x Mouse Logitech
(9, 7, 1);    -- Cable USB-C

-- Orden 10 (Ana)
INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad) VALUES
(10, 3, 4),   -- 4x Teclado Mecánico
(10, 10, 4);  -- 4x Adaptador HDMI

-- Orden 11 (Pedro)
INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad) VALUES
(11, 6, 1),   -- Auriculares Sony
(11, 3, 1),   -- Teclado Mecánico
(11, 2, 1);   -- Mouse Logitech

-- Orden 12 (Pedro)
INSERT INTO detalle_orden (orden_id, producto_id, orden_cantidad) VALUES
(12, 5, 2),   -- 2x Webcam HD
(12, 7, 2);   -- 2x Cable USB-C
