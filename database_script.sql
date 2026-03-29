-- =====================================================
-- SCRIPT DE BASE DE DATOS - SISTEMA CRUD FLASK
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
-- TABLA DE LOGS (Auditoría del Sistema)
-- =====================================================
CREATE TABLE IF NOT EXISTS logs (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    accion VARCHAR(50) NOT NULL,
    tabla_afectada VARCHAR(50),
    id_registro_afectado INT,
    descripcion TEXT,
    ip_address VARCHAR(45),
    fecha_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_usuario (id_usuario),
    INDEX idx_accion (accion),
    INDEX idx_tabla (tabla_afectada),
    INDEX idx_fecha (fecha_log),
    
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
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
-- CREAR VISTAS ÚTILES
-- =====================================================

-- Vista de productos con bajo stock
CREATE OR REPLACE VIEW vista_productos_bajo_stock AS
SELECT 
    id_producto,
    nombre,
    descripcion,
    precio,
    stock,
    categoria,
    CASE 
        WHEN stock = 0 THEN 'Agotado'
        WHEN stock <= 5 THEN 'Crítico'
        WHEN stock <= 10 THEN 'Bajo'
        ELSE 'Adecuado'
    END as estado_stock,
    (precio * stock) as valor_total
FROM productos 
WHERE activo = TRUE AND stock <= 10
ORDER BY stock ASC;

-- Vista de productos por categoría
CREATE OR REPLACE VIEW vista_productos_categoria AS
SELECT 
    categoria,
    COUNT(*) as total_productos,
    SUM(stock) as total_stock,
    SUM(precio * stock) as valor_total,
    AVG(precio) as precio_promedio
FROM productos 
WHERE activo = TRUE AND categoria IS NOT NULL
GROUP BY categoria
ORDER BY total_productos DESC;

-- Vista de préstamos activos
CREATE OR REPLACE VIEW vista_prestamos_activos AS
SELECT 
    p.id_prestamo,
    u.nombre as nombre_usuario,
    u.mail as email_usuario,
    pr.nombre as nombre_producto,
    p.fecha_prestamo,
    DATEDIFF(NOW(), p.fecha_prestamo) as dias_prestamo,
    CASE 
        WHEN DATEDIFF(NOW(), p.fecha_prestamo) > 30 THEN 'Vencido'
        ELSE 'Activo'
    END as estado_prestamo
FROM prestamos p
JOIN usuarios u ON p.id_usuario = u.id_usuario
JOIN productos pr ON p.id_producto = pr.id_producto
WHERE p.estado = 'activo'
ORDER BY p.fecha_prestamo;

-- =====================================================
-- CREAR PROCEDIMIENTOS ALMACENADOS
-- =====================================================

-- Procedimiento para actualizar stock
DELIMITER //
CREATE PROCEDURE sp_actualizar_stock(
    IN p_id_producto INT,
    IN p_cantidad INT,
    IN p_tipo VARCHAR(10) -- 'restar' o 'sumar'
)
BEGIN
    DECLARE v_stock_actual INT;
    DECLARE v_stock_nuevo INT;
    
    -- Obtener stock actual
    SELECT stock INTO v_stock_actual 
    FROM productos 
    WHERE id_producto = p_id_producto AND activo = TRUE;
    
    -- Calcular nuevo stock
    IF p_tipo = 'restar' THEN
        SET v_stock_nuevo = v_stock_actual - p_cantidad;
    ELSE
        SET v_stock_nuevo = v_stock_actual + p_cantidad;
    END IF;
    
    -- Validar que el stock no sea negativo
    IF v_stock_nuevo >= 0 THEN
        UPDATE productos 
        SET stock = v_stock_nuevo,
            fecha_actualizacion = NOW()
        WHERE id_producto = p_id_producto;
        
        SELECT TRUE as exito, v_stock_nuevo as stock_actual;
    ELSE
        SELECT FALSE as exito, v_stock_actual as stock_actual;
    END IF;
END //
DELIMITER ;

-- Procedimiento para obtener estadísticas
DELIMITER //
CREATE PROCEDURE sp_obtener_estadisticas()
BEGIN
    SELECT 
        COUNT(*) as total_productos,
        SUM(stock) as total_stock,
        SUM(precio * stock) as valor_total_inventario,
        COUNT(CASE WHEN stock <= 10 THEN 1 END) as productos_bajo_stock,
        AVG(precio) as precio_promedio,
        MAX(precio) as precio_maximo,
        MIN(precio) as precio_minimo
    FROM productos 
    WHERE activo = TRUE;
END //
DELIMITER ;

-- =====================================================
-- CREAR TRIGGERS PARA AUDITORÍA
-- =====================================================

-- Trigger para registrar cambios en productos
DELIMITER //
CREATE TRIGGER tr_productos_insert
AFTER INSERT ON productos
FOR EACH ROW
BEGIN
    INSERT INTO logs (accion, tabla_afectada, id_registro_afectado, descripcion)
    VALUES ('INSERT', 'productos', NEW.id_producto, 
            CONCAT('Producto creado: ', NEW.nombre, ' - Precio: ', NEW.precio));
END //

CREATE TRIGGER tr_productos_update
AFTER UPDATE ON productos
FOR EACH ROW
BEGIN
    INSERT INTO logs (accion, tabla_afectada, id_registro_afectado, descripcion)
    VALUES ('UPDATE', 'productos', NEW.id_producto, 
            CONCAT('Producto actualizado: ', NEW.nombre, ' - Stock: ', NEW.stock));
END //

CREATE TRIGGER tr_productos_delete
AFTER UPDATE ON productos
FOR EACH ROW
BEGIN
    IF NEW.activo = FALSE AND OLD.activo = TRUE THEN
        INSERT INTO logs (accion, tabla_afectada, id_registro_afectado, descripcion)
        VALUES ('DELETE', 'productos', NEW.id_producto, 
                CONCAT('Producto eliminado: ', NEW.nombre));
    END IF;
END //
DELIMITER ;

-- =====================================================
-- CREAR ÍNDICES ADICIONALES PARA MEJORAR RENDIMIENTO
-- =====================================================

-- Índices compuestos para búsquedas frecuentes
CREATE INDEX idx_producto_nombre_categoria ON productos(nombre, categoria);
CREATE INDEX idx_producto_precio_stock ON productos(precio, stock);
CREATE INDEX idx_prestamo_usuario_producto ON prestamos(id_usuario, id_producto);
CREATE INDEX idx_logs_usuario_fecha ON logs(id_usuario, fecha_log);

-- =====================================================
-- MOSTRAR INFORMACIÓN DE LA BASE DE DATOS
-- =====================================================

-- Mostrar todas las tablas creadas
SHOW TABLES;

-- Mostrar estructura de la tabla principal
DESCRIBE productos;

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
-- FIN DEL SCRIPT
-- =====================================================

/*
INSTRUCCIONES PARA EJECUTAR ESTE SCRIPT:

1. Abrir MySQL Workbench o línea de comandos MySQL
2. Copiar y pegar todo este script
3. Ejecutar el script completo
4. Verificar que todas las tablas se crearon correctamente

VERIFICACIÓN:
SELECT COUNT(*) as total_productos FROM productos WHERE activo = TRUE;
SELECT COUNT(*) as total_usuarios FROM usuarios WHERE activo = TRUE;
SELECT COUNT(*) as total_prestamos FROM prestamos WHERE estado = 'activo';

NOTAS:
- Este script crea la base de datos completa para el sistema CRUD
- Incluye datos de ejemplo para pruebas inmediatas
- Contiene vistas, procedimientos y triggers para funcionalidad avanzada
- La base de datos se llama "desarrollo_web"
- Todas las tablas usan InnoDB para soporte de transacciones
*/
