"""
Modelos de datos para el sistema de gestión de inventario de librería
Implementación de Programación Orientada a Objetos y colecciones
"""

import sqlite3
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime


class Producto:
    """
    Clase que representa un producto (libro) en el inventario.
    Utiliza diferentes tipos de colecciones para manejar datos eficientemente.
    """
    
    def __init__(self, id: int, nombre: str, cantidad: int, precio: float, 
                 autor: str, categoria: str, isbn: str = ""):
        """
        Inicializa un nuevo producto
        
        Args:
            id: Identificador único del producto
            nombre: Nombre del libro
            cantidad: Cantidad disponible en inventario
            precio: Precio del libro
            autor: Autor del libro
            categoria: Categoría del libro
            isbn: ISBN del libro (opcional)
        """
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
        self._autor = autor
        self._categoria = categoria
        self._isbn = isbn
        self._fecha_creacion = datetime.now()
        self._etiquetas = set()  # Conjunto para etiquetas únicas
        
    # Getters y Setters con validación
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor: str):
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor.strip()
    
    @property
    def cantidad(self) -> int:
        return self._cantidad
    
    @cantidad.setter
    def cantidad(self, valor: int):
        if valor < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self._cantidad = valor
    
    @property
    def precio(self) -> float:
        return self._precio
    
    @precio.setter
    def precio(self, valor: float):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = round(valor, 2)
    
    @property
    def autor(self) -> str:
        return self._autor
    
    @autor.setter
    def autor(self, valor: str):
        self._autor = valor.strip()
    
    @property
    def categoria(self) -> str:
        return self._categoria
    
    @categoria.setter
    def categoria(self, valor: str):
        self._categoria = valor.strip()
    
    @property
    def isbn(self) -> str:
        return self._isbn
    
    @isbn.setter
    def isbn(self, valor: str):
        self._isbn = valor.strip()
    
    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion
    
    @property
    def etiquetas(self) -> Set[str]:
        return self._etiquetas.copy()
    
    def agregar_etiqueta(self, etiqueta: str) -> None:
        """Agrega una etiqueta al conjunto de etiquetas"""
        self._etiquetas.add(etiqueta.strip().lower())
    
    def eliminar_etiqueta(self, etiqueta: str) -> None:
        """Elimina una etiqueta del conjunto"""
        self._etiquetas.discard(etiqueta.strip().lower())
    
    def a_diccionario(self) -> Dict:
        """Convierte el producto a un diccionario para almacenamiento"""
        return {
            'id': self._id,
            'nombre': self._nombre,
            'cantidad': self._cantidad,
            'precio': self._precio,
            'autor': self._autor,
            'categoria': self._categoria,
            'isbn': self._isbn,
            'fecha_creacion': self._fecha_creacion.isoformat(),
            'etiquetas': list(self._etiquetas)
        }
    
    def __str__(self) -> str:
        """Representación en texto del producto"""
        return f"Libro[{self._id}]: {self._nombre} - {self._autor} (${self._precio})"
    
    def __repr__(self) -> str:
        """Representación formal del producto"""
        return f"Producto(id={self._id}, nombre='{self._nombre}', cantidad={self._cantidad})"
    
    def __eq__(self, other) -> bool:
        """Compara productos por ID"""
        if isinstance(other, Producto):
            return self._id == other._id
        return False
    
    def __hash__(self) -> int:
        """Permite usar Producto como clave en diccionarios"""
        return hash(self._id)


class Inventario:
    """
    Clase que gestiona el inventario de productos utilizando colecciones
    para optimizar las operaciones de búsqueda y manejo de datos.
    """
    
    def __init__(self, db_path: str = "inventario.db"):
        """
        Inicializa el inventario y la conexión a la base de datos
        
        Args:
            db_path: Ruta del archivo de base de datos SQLite
        """
        self.db_path = db_path
        self._productos: Dict[int, Producto] = {}  # Diccionario principal: ID -> Producto
        self._categorias: Dict[str, Set[int]] = {}  # Diccionario: Categoría -> Conjunto de IDs
        self._autores: Dict[str, Set[int]] = {}  # Diccionario: Autor -> Conjunto de IDs
        self._isbn_index: Dict[str, int] = {}  # Diccionario: ISBN -> ID
        self._nombre_index: Dict[str, List[int]] = {}  # Diccionario: Nombre -> Lista de IDs (búsqueda por substring)
        
        # Inicializar base de datos
        self._inicializar_db()
        self._cargar_desde_db()
    
    def _inicializar_db(self) -> None:
        """Crea la tabla de productos si no existe"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    cantidad INTEGER NOT NULL DEFAULT 0,
                    precio REAL NOT NULL DEFAULT 0.0,
                    autor TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    isbn TEXT UNIQUE,
                    fecha_creacion TEXT NOT NULL,
                    etiquetas TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")
    
    def _cargar_desde_db(self) -> None:
        """Carga todos los productos desde la base de datos a las colecciones en memoria"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM productos ORDER BY id")
            filas = cursor.fetchall()
            
            for fila in filas:
                id, nombre, cantidad, precio, autor, categoria, isbn, fecha_creacion, etiquetas_str = fila
                
                # Crear producto
                producto = Producto(id, nombre, cantidad, precio, autor, categoria, isbn)
                
                # Cargar etiquetas
                if etiquetas_str:
                    etiquetas = etiquetas_str.split(',')
                    for etiqueta in etiquetas:
                        if etiqueta.strip():
                            producto.agregar_etiqueta(etiqueta.strip())
                
                # Agregar a las colecciones
                self._productos[id] = producto
                self._actualizar_indices(producto)
            
            conn.close()
            print(f"Cargados {len(self._productos)} productos desde la base de datos")
            
        except sqlite3.Error as e:
            print(f"Error al cargar desde la base de datos: {e}")
    
    def _actualizar_indices(self, producto: Producto) -> None:
        """Actualiza los índices de colecciones para búsquedas eficientes"""
        id_producto = producto.id
        
        # Actualizar índice de categorías
        if producto.categoria not in self._categorias:
            self._categorias[producto.categoria] = set()
        self._categorias[producto.categoria].add(id_producto)
        
        # Actualizar índice de autores
        if producto.autor not in self._autores:
            self._autores[producto.autor] = set()
        self._autores[producto.autor].add(id_producto)
        
        # Actualizar índice de ISBN
        if producto.isbn:
            self._isbn_index[producto.isbn] = id_producto
        
        # Actualizar índice de nombres (para búsqueda por substring)
        nombre_lower = producto.nombre.lower()
        for i in range(len(nombre_lower)):
            for j in range(i + 1, min(i + 20, len(nombre_lower) + 1)):  # Limitar longitud de substrings
                substring = nombre_lower[i:j]
                if substring not in self._nombre_index:
                    self._nombre_index[substring] = []
                if id_producto not in self._nombre_index[substring]:
                    self._nombre_index[substring].append(id_producto)
    
    def _eliminar_de_indices(self, producto: Producto) -> None:
        """Elimina un producto de todos los índices"""
        id_producto = producto.id
        
        # Eliminar de índice de categorías
        if producto.categoria in self._categorias:
            self._categorias[producto.categoria].discard(id_producto)
            if not self._categorias[producto.categoria]:
                del self._categorias[producto.categoria]
        
        # Eliminar de índice de autores
        if producto.autor in self._autores:
            self._autores[producto.autor].discard(id_producto)
            if not self._autores[producto.autor]:
                del self._autores[producto.autor]
        
        # Eliminar de índice de ISBN
        if producto.isbn and producto.isbn in self._isbn_index:
            del self._isbn_index[producto.isbn]
        
        # Eliminar de índice de nombres
        nombre_lower = producto.nombre.lower()
        substrings_a_eliminar = []
        for substring, ids in self._nombre_index.items():
            if id_producto in ids:
                ids.remove(id_producto)
                if not ids:
                    substrings_a_eliminar.append(substring)
        
        for substring in substrings_a_eliminar:
            del self._nombre_index[substring]
    
    def _guardar_en_db(self, producto: Producto) -> None:
        """Guarda o actualiza un producto en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            etiquetas_str = ','.join(producto.etiquetas) if producto.etiquetas else ''
            
            cursor.execute('''
                INSERT OR REPLACE INTO productos 
                (id, nombre, cantidad, precio, autor, categoria, isbn, fecha_creacion, etiquetas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                producto.id,
                producto.nombre,
                producto.cantidad,
                producto.precio,
                producto.autor,
                producto.categoria,
                producto.isbn,
                producto.fecha_creacion.isoformat(),
                etiquetas_str
            ))
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Error al guardar en la base de datos: {e}")
    
    def _eliminar_de_db(self, id_producto: int) -> None:
        """Elimina un producto de la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Error al eliminar de la base de datos: {e}")
    
    def agregar_producto(self, nombre: str, cantidad: int, precio: float, 
                       autor: str, categoria: str, isbn: str = "") -> Producto:
        """
        Agrega un nuevo producto al inventario
        
        Args:
            nombre: Nombre del libro
            cantidad: Cantidad inicial
            precio: Precio del libro
            autor: Autor del libro
            categoria: Categoría del libro
            isbn: ISBN (opcional)
            
        Returns:
            El producto creado
        """
        # Generar nuevo ID
        nuevo_id = max(self._productos.keys(), default=0) + 1
        
        # Crear producto
        producto = Producto(nuevo_id, nombre, cantidad, precio, autor, categoria, isbn)
        
        # Agregar a colecciones
        self._productos[nuevo_id] = producto
        self._actualizar_indices(producto)
        
        # Guardar en base de datos
        self._guardar_en_db(producto)
        
        return producto
    
    def eliminar_producto(self, id_producto: int) -> bool:
        """
        Elimina un producto del inventario
        
        Args:
            id_producto: ID del producto a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no se encontró
        """
        if id_producto not in self._productos:
            return False
        
        producto = self._productos[id_producto]
        
        # Eliminar de índices
        self._eliminar_de_indices(producto)
        
        # Eliminar del diccionario principal
        del self._productos[id_producto]
        
        # Eliminar de base de datos
        self._eliminar_de_db(id_producto)
        
        return True
    
    def actualizar_producto(self, id_producto: int, **kwargs) -> bool:
        """
        Actualiza los atributos de un producto
        
        Args:
            id_producto: ID del producto a actualizar
            **kwargs: Atributos a actualizar (nombre, cantidad, precio, autor, categoria, isbn)
            
        Returns:
            True si se actualizó correctamente, False si no se encontró
        """
        if id_producto not in self._productos:
            return False
        
        producto = self._productos[id_producto]
        
        # Eliminar de índices antiguos
        self._eliminar_de_indices(producto)
        
        # Actualizar atributos
        for atributo, valor in kwargs.items():
            if hasattr(producto, f'_{atributo}'):
                setattr(producto, atributo, valor)
        
        # Actualizar índices nuevos
        self._actualizar_indices(producto)
        
        # Guardar en base de datos
        self._guardar_en_db(producto)
        
        return True
    
    def buscar_por_id(self, id_producto: int) -> Optional[Producto]:
        """Busca un producto por su ID"""
        return self._productos.get(id_producto)
    
    def buscar_por_nombre(self, nombre: str, exacto: bool = False) -> List[Producto]:
        """
        Busca productos por nombre
        
        Args:
            nombre: Nombre o parte del nombre a buscar
            exacto: Si True, busca coincidencia exacta; si False, busca substring
            
        Returns:
            Lista de productos que coinciden
        """
        resultados = []
        nombre_lower = nombre.lower()
        
        if exacto:
            # Búsqueda exacta
            for producto in self._productos.values():
                if producto.nombre.lower() == nombre_lower:
                    resultados.append(producto)
        else:
            # Búsqueda por substring usando índice
            if nombre_lower in self._nombre_index:
                for id_producto in self._nombre_index[nombre_lower]:
                    if id_producto in self._productos:
                        resultados.append(self._productos[id_producto])
        
        return resultados
    
    def buscar_por_autor(self, autor: str) -> List[Producto]:
        """Busca todos los libros de un autor específico"""
        resultados = []
        
        if autor in self._autores:
            for id_producto in self._autores[autor]:
                if id_producto in self._productos:
                    resultados.append(self._productos[id_producto])
        
        return resultados
    
    def buscar_por_categoria(self, categoria: str) -> List[Producto]:
        """Busca todos los libros de una categoría específica"""
        resultados = []
        
        if categoria in self._categorias:
            for id_producto in self._categorias[categoria]:
                if id_producto in self._productos:
                    resultados.append(self._productos[id_producto])
        
        return resultados
    
    def buscar_por_isbn(self, isbn: str) -> Optional[Producto]:
        """Busca un producto por su ISBN"""
        if isbn in self._isbn_index:
            id_producto = self._isbn_index[isbn]
            return self._productos.get(id_producto)
        return None
    
    def obtener_todos(self) -> List[Producto]:
        """Retorna todos los productos del inventario"""
        return list(self._productos.values())
    
    def obtener_categorias(self) -> List[str]:
        """Retorna todas las categorías disponibles"""
        return sorted(self._categorias.keys())
    
    def obtener_autores(self) -> List[str]:
        """Retorna todos los autores disponibles"""
        return sorted(self._autores.keys())
    
    def obtener_estadisticas(self) -> Dict:
        """
        Retorna estadísticas del inventario usando diferentes tipos de colecciones
        
        Returns:
            Diccionario con estadísticas diversas
        """
        if not self._productos:
            return {
                'total_productos': 0,
                'total_categorias': 0,
                'total_autores': 0,
                'valor_total_inventario': 0.0,
                'cantidad_total': 0,
                'precio_promedio': 0.0,
                'categorias_mas_populares': [],
                'autores_mas_productivos': []
            }
        
        # Estadísticas básicas
        total_productos = len(self._productos)
        total_categorias = len(self._categorias)
        total_autores = len(self._autores)
        
        # Calcular totales
        valor_total = sum(p.precio * p.cantidad for p in self._productos.values())
        cantidad_total = sum(p.cantidad for p in self._productos.values())
        precio_promedio = sum(p.precio for p in self._productos.values()) / total_productos
        
        # Categorías más populares (conteo usando diccionario)
        categorias_count = {}
        for categoria, ids in self._categorias.items():
            categorias_count[categoria] = len(ids)
        
        categorias_populares = sorted(categorias_count.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Autores más productivos (conteo usando diccionario)
        autores_count = {}
        for autor, ids in self._autores.items():
            autores_count[autor] = len(ids)
        
        autores_productivos = sorted(autores_count.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_productos': total_productos,
            'total_categorias': total_categorias,
            'total_autores': total_autores,
            'valor_total_inventario': round(valor_total, 2),
            'cantidad_total': cantidad_total,
            'precio_promedio': round(precio_promedio, 2),
            'categorias_mas_populares': [(cat, count) for cat, count in categorias_populares],
            'autores_mas_productivos': [(aut, count) for aut, count in autores_productivos]
        }
    
    def exportar_a_lista_tuplas(self) -> List[Tuple]:
        """
        Exporta el inventario como una lista de tuplas
        
        Returns:
            Lista de tuplas con (id, nombre, cantidad, precio, autor, categoria, isbn)
        """
        return [
            (p.id, p.nombre, p.cantidad, p.precio, p.autor, p.categoria, p.isbn)
            for p in self._productos.values()
        ]
    
    def productos_bajo_stock(self, umbral: int = 5) -> List[Producto]:
        """
        Retorna productos con stock bajo
        
        Args:
            umbral: Umbral de stock bajo
            
        Returns:
            Lista de productos con cantidad menor al umbral
        """
        return [p for p in self._productos.values() if p.cantidad <= umbral]
    
    def __len__(self) -> int:
        """Retorna el número total de productos"""
        return len(self._productos)
    
    def __str__(self) -> str:
        """Representación en texto del inventario"""
        return f"Inventario con {len(self._productos)} productos"
