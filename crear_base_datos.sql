-- =====================================================
-- SCRIPT PARA CREAR BASE DE DATOS - SISTEMA CRUD FLASK
-- Semana 16 - Desarrollo Web Avanzado
-- =====================================================

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS desarrollo_web 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE desarrollo_web;

-- =====================================================
-- TABLA DE USUARIOS (Sistema de Autenticación)
-- =====================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    mail VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_mail (mail),
    INDEX idx_activo (activo)
) ENGINE=InnoDB;

-- =====================================================
-- TABLA DE CATEGORÍAS
-- =====================================================
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_nombre (nombre),
    INDEX idx_activa (activa)
) ENGINE=InnoDB;

-- =====================================================
-- TABLA DE PRODUCTOS (Sistema CRUD Principal)
-- =====================================================
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    categoria VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_nombre (nombre),
    INDEX idx_categoria (categoria),
    INDEX idx_activo (activo),
    INDEX idx_stock (stock),
    INDEX idx_precio (precio),
    
    CONSTRAINT chk_precio_positivo CHECK (precio > 0),
    CONSTRAINT chk_stock_no_negativo CHECK (stock >= 0),
    CONSTRAINT chk_nombre_no_vacio CHECK (nombre <> '')
) ENGINE=InnoDB;

-- =====================================================
-- TABLA DE PRÉSTAMOS (Sistema de Biblioteca)
-- =====================================================
CREATE TABLE IF NOT EXISTS prestamos (
    id_prestamo INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion TIMESTAMP NULL,
    estado ENUM('activo', 'devuelto', 'vencido') DEFAULT 'activo',
    observaciones TEXT,
    
    INDEX idx_usuario (id_usuario),
    INDEX idx_producto (id_producto),
    INDEX idx_estado (estado),
    INDEX idx_fecha_prestamo (fecha_prestamo),
    
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =====================================================
-- INSERTAR DATOS DE EJEMPLO
-- =====================================================

-- Insertar categorías de ejemplo
INSERT IGNORE INTO categorias (nombre, descripcion) VALUES
('Tecnología', 'Productos tecnológicos y electrónicos'),
('Libros', 'Libros y material educativo'),
('Hogar', 'Artículos para el hogar y decoración'),
('Ropa', 'Vestimenta y accesorios'),
('Alimentos', 'Productos alimenticios y bebidas'),
('Deportes', 'Artículos deportivos y fitness'),
('Oficina', 'Suministros de oficina y papelería'),
('Juguetes', 'Juguetes y juegos educativos'),
('Salud', 'Productos de salud y bienestar'),
('Música', 'Instrumentos musicales y accesorios');

-- Insertar usuarios de ejemplo
INSERT IGNORE INTO usuarios (nombre, mail, password, activo) VALUES
('Administrador', 'admin@ejemplo.com', 'admin123', TRUE),
('Juan Pérez', 'juan@ejemplo.com', 'user123', TRUE),
('María García', 'maria@ejemplo.com', 'user123', TRUE),
('Carlos López', 'carlos@ejemplo.com', 'user123', TRUE),
('Ana Martínez', 'ana@ejemplo.com', 'user123', TRUE);

-- Insertar productos de ejemplo
INSERT IGNORE INTO productos (nombre, descripcion, precio, stock, categoria, activo) VALUES
('Laptop HP Pavilion', 'Laptop de 15.6 pulgadas, Intel i5, 8GB RAM, 256GB SSD', 599.99, 15, 'Tecnología', TRUE),
('Mouse Inalámbrico Logitech', 'Mouse inalámbrico ergonómico con receptor USB', 25.99, 45, 'Tecnología', TRUE),
('Teclado Mecánico RGB', 'Teclado mecánico con retroiluminación RGB', 79.99, 30, 'Tecnología', TRUE),
('Monitor 24 pulgadas', 'Monitor LED Full HD 1080p, 75Hz', 189.99, 8, 'Tecnología', TRUE),
('Auriculares Bluetooth', 'Auriculares inalámbricos con cancelación de ruido', 49.99, 25, 'Tecnología', TRUE),

('Python para Principiantes', 'Libro introductorio de programación Python', 29.99, 20, 'Libros', TRUE),
('JavaScript Avanzado', 'Guía completa de JavaScript moderno', 39.99, 15, 'Libros', TRUE),
('Flask Web Development', 'Libro de desarrollo web con Flask', 44.99, 12, 'Libros', TRUE),
('Algoritmos y Estructuras', 'Libro de algoritmos y estructuras de datos', 54.99, 8, 'Libros', TRUE),
('Base de Datos SQL', 'Guía completa de bases de datos SQL', 34.99, 18, 'Libros', TRUE),

('Silla de Oficina', 'Silla ergonómica con soporte lumbar', 149.99, 5, 'Oficina', TRUE),
('Escritorio de Madera', 'Escritorio de 120x60cm con cajones', 199.99, 3, 'Oficina', TRUE),
('Lámpara LED Escritorio', 'Lámpara LED ajustable para escritorio', 29.99, 22, 'Oficina', TRUE),
('Organizador de Archivos', 'Organizador plástico con 6 compartimentos', 15.99, 35, 'Oficina', TRUE),
('Calculadora Científica', 'Calculadora científica con funciones avanzadas', 19.99, 40, 'Oficina', TRUE),

('Botella de Agua', 'Botella de acero inoxidable 500ml', 12.99, 50, 'Deportes', TRUE),
('Cinta de Correr', 'Cinta de medición profesional 5m', 8.99, 60, 'Deportes', TRUE),
('Mancuernas 5kg', 'Par de mancuernas ajustables 5kg', 39.99, 10, 'Deportes', TRUE),
('Yoga Mat', 'Colchonilla de yoga antideslizante', 24.99, 25, 'Deportes', TRUE),
('Bandas de Resistencia', 'Set de 5 bandas elásticas', 19.99, 30, 'Deportes', TRUE),

('Cafetera de Goteo', 'Cafetera programable para 12 tazas', 89.99, 7, 'Hogar', TRUE),
('Tostadora', 'Tostadora de 2 rebanadas con ajuste', 34.99, 18, 'Hogar', TRUE),
('Licuadora', 'Licuadora de 1000W con vasos múltiples', 79.99, 12, 'Hogar', TRUE),
('Plancha de Ropa', 'Plancha de vapor con cerámica', 44.99, 20, 'Hogar', TRUE),
('Ventilador de Mesa', 'Ventilador oscilante 3 velocidades', 29.99, 15, 'Hogar', TRUE),

('Camiseta Algodón', 'Camiseta de algodón 100% talla M', 19.99, 40, 'Ropa', TRUE),
('Pantalón Vaquero', 'Pantalón vaquero talla 32', 49.99, 25, 'Ropa', TRUE),
('Chaqueta Impermeable', 'Chaqueta impermeable con capucha', 69.99, 15, 'Ropa', TRUE),
('Zapatillas Deportivas', 'Zapatillas running talla 42', 79.99, 20, 'Ropa', TRUE),
('Calcetines Deportivos', 'Pack 3 pares de calcetines deportivos', 12.99, 55, 'Ropa', TRUE),

('Arroz Blanco', 'Bolsa de arroz blanco 1kg', 2.99, 100, 'Alimentos', TRUE),
('Pasta Italiana', 'Paquete de pasta 500g', 1.99, 150, 'Alimentos', TRUE),
('Aceite de Oliva', 'Botella de aceite de oliva extra virgen 750ml', 8.99, 30, 'Alimentos', TRUE),
('Café en Grano', 'Bolsa de café en grano 500g', 12.99, 25, 'Alimentos', TRUE),
('Agua Mineral', 'Pack 6 botellas de agua mineral 1.5L', 4.99, 80, 'Alimentos', TRUE),

('Guitarra Acústica', 'Guitarra acústica de 6 cuerdas', 149.99, 4, 'Música', TRUE),
('Teclado Musical', 'Teclado musical de 61 teclas', 89.99, 6, 'Música', TRUE),
('Batería Electrónica', 'Batería electrónica con pads', 299.99, 2, 'Música', TRUE),
('Micrófono USB', 'Micrófono condensador USB', 59.99, 8, 'Música', TRUE),
('Afinador Digital', 'Afinador digital para guitarra', 14.99, 35, 'Música', TRUE),

('Kit de Lego', 'Set de Lego 500 piezas', 39.99, 12, 'Juguetes', TRUE),
('Rompecabezas 1000p', 'Rompecabezas de 1000 piezas', 15.99, 28, 'Juguetes', TRUE),
('Muñeca de Peluche', 'Muñeca de peluche 30cm', 19.99, 20, 'Juguetes', TRUE),
('Coche Teledirigido', 'Coche teledirigido 2.4GHz', 49.99, 8, 'Juguetes', TRUE),
('Juego de Mesa', 'Juego de mesa familiar', 24.99, 15, 'Juguetes', TRUE),

('Vitaminas C', 'Suplemento de vitamina C 60 tabletas', 9.99, 45, 'Salud', TRUE),
('Termómetro Digital', 'Termómetro digital clínico', 12.99, 30, 'Salud', TRUE),
('Tensiómetro', 'Tensiómetro de brazo automático', 39.99, 10, 'Salud', TRUE),
('Pulsera Fitness', 'Pulsera con monitor de actividad', 29.99, 18, 'Salud', TRUE),
('Kit Primeros Auxilios', 'Kit básico de primeros auxilios', 19.99, 25, 'Salud', TRUE);

-- Insertar préstamos de ejemplo
INSERT IGNORE INTO prestamos (id_usuario, id_producto, estado) VALUES
(2, 6, 'activo'),  -- Juan Pérez -> Python para Principiantes
(2, 7, 'activo'),  -- Juan Pérez -> JavaScript Avanzado
(3, 8, 'activo'),  -- María García -> Flask Web Development
(3, 9, 'devuelto'), -- María García -> Algoritmos y Estructuras
(4, 10, 'activo'), -- Carlos López -> Base de Datos SQL
(5, 11, 'activo'); -- Ana Martínez -> Silla de Oficina

-- =====================================================
-- MOSTRAR RESULTADOS
-- =====================================================

-- Mostrar todas las tablas creadas
SHOW TABLES;

-- Mostrar estadísticas iniciales
SELECT 
    'ESTADÍSTICAS INICIALES' as tipo,
    COUNT(*) as total_productos,
    SUM(stock) as total_stock,
    SUM(precio * stock) as valor_total,
    AVG(precio) as precio_promedio
FROM productos 
WHERE activo = TRUE;

-- =====================================================
-- INSTRUCCIONES DE USO
-- =====================================================

/*
COMO EJECUTAR ESTE SCRIPT:

1. Abrir MySQL Workbench o línea de comandos MySQL
2. Copiar y pegar todo este script
3. Ejecutar el script completo
4. Verificar que las tablas se crearon correctamente

VERIFICACIÓN RÁPIDA:
SELECT COUNT(*) as total_productos FROM productos WHERE activo = TRUE;
SELECT COUNT(*) as total_usuarios FROM usuarios WHERE activo = TRUE;
SELECT COUNT(*) as total_categorias FROM categorias WHERE activa = TRUE;

DATOS DE ACCESO DE EJEMPLO:
- Usuario: admin@ejemplo.com / Contraseña: admin123
- Usuario: juan@ejemplo.com / Contraseña: user123
- Usuario: maria@ejemplo.com / Contraseña: user123

NOTAS:
- Base de datos: desarrollo_web
- Motor: InnoDB (soporte de transacciones)
- Codificación: utf8mb4 (soporte completo UTF-8)
- Incluye 50 productos de ejemplo en 10 categorías
- Sistema completo para pruebas inmediatas
*/
