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
-- DATOS DE PRUEBA USUARIOS
-- =========================
INSERT INTO usuarios (nombre, mail, password) VALUES
('Administrador', 'admin@tienda.com', '1234'),
('Beivy Rivera', 'beivy@tienda.com', '1234');

-- =========================
-- DATOS DE PRUEBA PRODUCTOS
-- =========================
INSERT INTO productos (nombre, descripcion, precio, stock) VALUES
('Laptop HP', 'Laptop para oficina', 850.00, 10),
('Mouse Logitech', 'Mouse inalámbrico', 25.50, 50),
('Teclado Mecánico', 'Teclado RGB', 70.00, 20);

-- =========================
-- DATOS DE PRUEBA CLIENTES
-- =========================
INSERT INTO clientes (nombre, apellido, correo, telefono, direccion) VALUES
('Juan', 'Pérez', 'juan@email.com', '0991111111', 'Quito'),
('María', 'López', 'maria@email.com', '0982222222', 'Latacunga');