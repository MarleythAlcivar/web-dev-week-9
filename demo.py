"""
Script de demostración del Sistema de Gestión de Inventario
Muestra el uso de las clases y colecciones implementadas
"""

from models import Inventario, Producto
from typing import List


def demo_sistema_inventario():
    """
    Demostración completa del sistema de gestión de inventario
    """
    print("🚀 DEMOSTRACIÓN DEL SISTEMA DE GESTIÓN DE INVENTARIO")
    print("=" * 60)
    
    # 1. Crear instancia del inventario
    print("\n1️⃣ Inicializando el sistema de inventario...")
    inventario = Inventario()
    print(f"   📊 Inventario creado con {len(inventario)} productos")
    
    # 2. Agregar productos de ejemplo
    print("\n2️⃣ Agregando productos de ejemplo...")
    
    productos_demo = [
        {
            "nombre": "Programación en Python",
            "cantidad": 15,
            "precio": 45.99,
            "autor": "Juan Pérez",
            "categoria": "Ciencias Exactas",
            "isbn": "978-1234567890"
        },
        {
            "nombre": "Cien Años de Soledad",
            "cantidad": 8,
            "precio": 25.50,
            "autor": "Gabriel García Márquez",
            "categoria": "Literatura Latinoamericana",
            "isbn": "978-0987654321"
        },
        {
            "nombre": "Cálculo Diferencial",
            "cantidad": 12,
            "precio": 38.75,
            "autor": "María González",
            "categoria": "Ciencias Exactas",
            "isbn": "978-1122334455"
        },
        {
            "nombre": "Historia del Arte",
            "cantidad": 6,
            "precio": 52.30,
            "autor": "Roberto Silva",
            "categoria": "Artes y Humanidades",
            "isbn": "978-5566778899"
        },
        {
            "nombre": "Física Cuántica",
            "cantidad": 4,
            "precio": 67.80,
            "autor": "Ana Martínez",
            "categoria": "Ciencias Exactas",
            "isbn": "978-9988776655"
        }
    ]
    
    productos_creados = []
    for datos in productos_demo:
        producto = inventario.agregar_producto(**datos)
        productos_creados.append(producto)
        print(f"   ✅ Agregado: {producto.nombre} (ID: {producto.id})")
    
    # 3. Demostrar uso de colecciones
    print(f"\n3️⃣ Demostración de colecciones y búsquedas...")
    
    # Búsqueda por nombre (substring)
    print("\n   🔍 Búsqueda por substring 'Python':")
    resultados = inventario.buscar_por_nombre("Python")
    for p in resultados:
        print(f"      📖 {p.nombre} - {p.autor}")
    
    # Búsqueda por categoría
    print("\n   📂 Búsqueda por categoría 'Ciencias Exactas':")
    resultados = inventario.buscar_por_categoria("Ciencias Exactas")
    print(f"      📊 Se encontraron {len(resultados)} libros:")
    for p in resultados:
        print(f"         📚 {p.nombre} - ${p.precio:.2f}")
    
    # Búsqueda por autor
    print("\n   👥 Búsqueda por autor 'Gabriel García Márquez':")
    resultados = inventario.buscar_por_autor("Gabriel García Márquez")
    for p in resultados:
        print(f"      📖 {p.nombre} - Categoría: {p.categoria}")
    
    # 4. Demostrar operaciones CRUD
    print(f"\n4️⃣ Demostración de operaciones CRUD...")
    
    # Actualizar un producto
    print("\n   ✏️ Actualizando cantidad de 'Física Cuántica':")
    producto_actualizar = inventario.buscar_por_nombre("Física Cuántica")[0]
    print(f"      📊 Antes: {producto_actualizar.cantidad} unidades")
    
    inventario.actualizar_producto(producto_actualizar.id, cantidad=10)
    producto_actualizado = inventario.buscar_por_id(producto_actualizar.id)
    print(f"      📊 Después: {producto_actualizado.cantidad} unidades")
    
    # Agregar etiquetas a un producto
    print("\n   🏷️ Agregando etiquetas a 'Programación en Python':")
    producto_etiquetas = inventario.buscar_por_nombre("Programación en Python")[0]
    producto_etiquetas.agregar_etiqueta("programación")
    producto_etiquetas.agregar_etiqueta("python")
    producto_etiquetas.agregar_etiqueta("desarrollo")
    print(f"      🏷️ Etiquetas: {', '.join(producto_etiquetas.etiquetas)}")
    
    # 5. Demostrar estadísticas
    print(f"\n5️⃣ Estadísticas del inventario...")
    stats = inventario.obtener_estadisticas()
    
    print(f"   📈 Total de productos: {stats['total_productos']}")
    print(f"   📂 Total de categorías: {stats['total_categorias']}")
    print(f"   👥 Total de autores: {stats['total_autores']}")
    print(f"   💰 Valor total del inventario: ${stats['valor_total_inventario']:,.2f}")
    print(f"   📦 Cantidad total de unidades: {stats['cantidad_total']}")
    print(f"   💵 Precio promedio: ${stats['precio_promedio']:.2f}")
    
    print(f"\n   🏆 Categorías más populares:")
    for categoria, count in stats['categorias_mas_populares']:
        print(f"      📚 {categoria}: {count} libros")
    
    print(f"\n   ✍️ Autores más productivos:")
    for autor, count in stats['autores_mas_productivos']:
        print(f"      👤 {autor}: {count} libros")
    
    # 6. Demostrar productos con bajo stock
    print(f"\n6️⃣ Control de stock bajo...")
    productos_bajo_stock = inventario.productos_bajo_stock(umbral=5)
    
    if productos_bajo_stock:
        print(f"   ⚠️ Productos con bajo stock (≤ 5 unidades):")
        for p in productos_bajo_stock:
            print(f"      📖 {p.nombre} - Stock: {p.cantidad}")
    else:
        print("   ✅ No hay productos con bajo stock")
    
    # 7. Demostrar exportación de datos
    print(f"\n7️⃣ Exportación de datos...")
    
    # Exportar como lista de tuplas
    tuplas = inventario.exportar_a_lista_tuplas()
    print(f"   📋 Exportados {len(tuplas)} productos como tuplas")
    print(f"   📝 Formato: (ID, Nombre, Cantidad, Precio, Autor, Categoría, ISBN)")
    
    # Mostrar primeras 3 tuplas como ejemplo
    print(f"   📄 Ejemplos:")
    for i, tupla in enumerate(tuplas[:3], 1):
        print(f"      {i}. {tupla}")
    
    # 8. Demostrar tipos de colecciones utilizadas
    print(f"\n8️⃣ Tipos de colecciones utilizadas en el sistema...")
    
    print(f"   🗂️ Diccionarios:")
    print(f"      - _productos: Dict[int, Producto] - Almacenamiento principal")
    print(f"      - _categorias: Dict[str, Set[int]] - Índice por categoría")
    print(f"      - _autores: Dict[str, Set[int]] - Índice por autor")
    print(f"      - _isbn_index: Dict[str, int] - Índice por ISBN")
    print(f"      - _nombre_index: Dict[str, List[int]] - Índice de nombres")
    
    print(f"   🔢 Conjuntos (Sets):")
    print(f"      - _etiquetas: Set[str] - Etiquetas únicas por producto")
    print(f"      - Índices: Set[int> - IDs únicos por categoría/autor")
    
    print(f"   📋 Listas:")
    print(f"      - Resultados de búsqueda: List[Producto]")
    print(f"      - Índice de nombres: List[int> por substring")
    
    print(f"   📦 Tuplas:")
    print(f"      - Exportación: List[Tuple] - Formato de datos para exportación")
    
    # 9. Demostrar persistencia
    print(f"\n9️⃣ Persistencia de datos...")
    print(f"   💾 Los datos se guardan automáticamente en 'inventario.db'")
    print(f"   🔄 Al reiniciar el sistema, los datos se cargan desde la base de datos")
    
    # 10. Resumen final
    print(f"\n🎉 DEMOSTRACIÓN COMPLETADA")
    print("=" * 60)
    print(f"   📚 Sistema de gestión de inventario funcional")
    print(f"   🏗️ Arquitectura POO con colecciones optimizadas")
    print(f"   💾 Base de datos SQLite integrada")
    print(f"   🔍 Búsquedas eficientes con múltiples índices")
    print(f"   📊 Estadísticas y reportes automáticos")
    print(f"   🔄 Operaciones CRUD completas")
    print("=" * 60)


def demo_menu_consola():
    """
    Demostración del menú interactivo de consola
    """
    print("\n🖥️ DEMOSTRACIÓN DEL MENÚ INTERACTIVO")
    print("=" * 60)
    print("Para ejecutar el menú interactivo completo:")
    print("   python menu_interactivo.py")
    print("\nOpciones disponibles:")
    print("   1. 📖 Agregar nuevo producto")
    print("   2. 🗑️ Eliminar producto")
    print("   3. ✏️ Actualizar producto")
    print("   4. 🔍 Buscar producto")
    print("   5. 📋 Mostrar todos los productos")
    print("   6. 📊 Ver estadísticas del inventario")
    print("   7. 📂 Ver categorías disponibles")
    print("   8. 👥 Ver autores disponibles")
    print("   9. ⚠️ Productos con bajo stock")
    print("   10. 📚 Buscar por categoría")
    print("   11. ✍️ Buscar por autor")
    print("   12. 💾 Exportar datos")
    print("   0. 🚪 Salir")


def demo_api_web():
    """
    Demostración de la API web y Flask
    """
    print("\n🌐 DEMOSTRACIÓN DE LA API WEB")
    print("=" * 60)
    print("Para ejecutar la aplicación web:")
    print("   python app.py")
    print("\nEndpoints disponibles:")
    print("   📡 GET  /api/productos - Obtener todos los productos")
    print("   📡 POST /api/producto - Crear nuevo producto")
    print("   📡 PUT  /api/producto/<id> - Actualizar producto")
    print("   📡 DELETE /api/producto/<id> - Eliminar producto")
    print("   📡 GET  /api/buscar - Buscar productos")
    print("   📡 GET  /api/estadisticas - Obtener estadísticas")
    print("\nRutas web:")
    print("   🏠 GET  / - Página principal")
    print("   📚 GET  /libros - Catálogo de libros")
    print("   📂 GET  /catalogo - Catálogo completo")
    print("   📖 GET  /libro/<id> - Detalles del libro")
    print("   👤 GET  /usuario/<nombre> - Perfil de autor")


if __name__ == "__main__":
    # Ejecutar demostración principal
    demo_sistema_inventario()
    
    # Mostrar información sobre otras interfaces
    demo_menu_consola()
    demo_api_web()
    
    print(f"\n🚀 ¡Sistema listo para usar!")
    print(f"   📊 Ejecuta 'python menu_interactivo.py' para el menú de consola")
    print(f"   🌐 Ejecuta 'python app.py' para la interfaz web")
    print(f"   📚 Revisa 'README.md' para más información")
