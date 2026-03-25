DROP DATABASE IF EXISTS tienda_online;
CREATE DATABASE tienda_online;
USE tienda_online;

-- =========================
-- TABLA USUARIOS
-- =========================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    mail VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- =========================
-- TABLA CLIENTES
-- =========================
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    direccion VARCHAR(255)
);

-- =========================
-- TABLA PRODUCTOS
-- =========================
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

-- =========================
-- TABLA FACTURAS
-- =========================
CREATE TABLE facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_cliente INT NOT NULL,
    id_usuario INT NOT NULL,
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- =========================
-- TABLA DETALLE_FACTURA
-- =========================
CREATE TABLE detalle_factura (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_factura INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- =========================
-- DATOS DE PRUEBA USUARIOS
-- =========================
INSERT INTO usuarios (nombre, mail, password) VALUES
('Administrador', 'admin@tienda.com', '1234'),
('Beivy Rivera', 'beivy@tienda.com', '1234');

-- =========================
-- DATOS DE PRUEBA CLIENTES
-- =========================
INSERT INTO clientes (nombre, apellido, correo, telefono, direccion) VALUES
('Juan', 'Pérez', 'juan@email.com', '0991111111', 'Quito'),
('María', 'López', 'maria@email.com', '0982222222', 'Latacunga');

-- =========================
-- DATOS DE PRUEBA PRODUCTOS
-- =========================
INSERT INTO productos (nombre, descripcion, precio, stock) VALUES
('Laptop HP', 'Laptop para oficina', 850.00, 10),
('Mouse Logitech', 'Mouse inalámbrico', 25.50, 50),
('Teclado Mecánico', 'Teclado RGB', 70.00, 20);

-- =========================
-- DATOS DE PRUEBA FACTURAS
-- =========================
INSERT INTO facturas (id_cliente, id_usuario, total) VALUES
(1, 1, 875.50),
(2, 2, 70.00);

-- =========================
-- DATOS DE PRUEBA DETALLE_FACTURA
-- =========================
INSERT INTO detalle_factura (id_factura, id_producto, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 1, 850.00, 850.00),
(1, 2, 1, 25.50, 25.50),
(2, 3, 1, 70.00, 70.00);