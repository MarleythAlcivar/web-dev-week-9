"""
Interfaz de usuario interactiva para el sistema de gestión de inventario
Proporciona un menú de consola para realizar operaciones CRUD
"""

from models import Inventario, Producto
from typing import List, Optional
import os


class MenuInventario:
    """
    Clase que maneja la interfaz de usuario del sistema de inventario
    """
    
    def __init__(self):
        """Inicializa el menú y el inventario"""
        self.inventario = Inventario()
        self.opciones_menu = {
            '1': self.agregar_producto,
            '2': self.eliminar_producto,
            '3': self.actualizar_producto,
            '4': self.buscar_producto,
            '5': self.mostrar_todos,
            '6': self.mostrar_estadisticas,
            '7': self.mostrar_categorias,
            '8': self.mostrar_autores,
            '9': self.productos_bajo_stock,
            '10': self.buscar_por_categoria,
            '11': self.buscar_por_autor,
            '12': self.exportar_datos,
            '0': self.salir
        }
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_header(self):
        """Muestra el encabezado del sistema"""
        print("=" * 60)
        print("📚 SISTEMA AVANZADO DE GESTIÓN DE INVENTARIO - LIBRERÍA 📚")
        print("=" * 60)
        print(f"Total de productos en inventario: {len(self.inventario)}")
        print("=" * 60)
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de opciones"""
        print("\n🔧 MENÚ PRINCIPAL 🔧")
        print("-" * 40)
        print("1. 📖 Agregar nuevo producto")
        print("2. 🗑️  Eliminar producto")
        print("3. ✏️  Actualizar producto")
        print("4. 🔍 Buscar producto")
        print("5. 📋 Mostrar todos los productos")
        print("6. 📊 Ver estadísticas del inventario")
        print("7. 📂 Ver categorías disponibles")
        print("8. 👥 Ver autores disponibles")
        print("9. ⚠️  Productos con bajo stock")
        print("10. 📚 Buscar por categoría")
        print("11. ✍️  Buscar por autor")
        print("12. 💾 Exportar datos")
        print("0. 🚪 Salir")
        print("-" * 40)
    
    def obtener_input(self, mensaje: str, obligatorio: bool = True) -> str:
        """
        Obtiene input del usuario con validación
        
        Args:
            mensaje: Mensaje a mostrar
            obligatorio: Si es obligatorio no puede estar vacío
            
        Returns:
            El valor ingresado por el usuario
        """
        while True:
            valor = input(mensaje).strip()
            if valor or not obligatorio:
                return valor
            print("❌ Este campo es obligatorio. Por favor ingrese un valor.")
    
    def obtener_numero(self, mensaje: str, min_val: Optional[float] = None, 
                      max_val: Optional[float] = None, entero: bool = False) -> float:
        """
        Obtiene un número del usuario con validación
        
        Args:
            mensaje: Mensaje a mostrar
            min_val: Valor mínimo permitido
            max_val: Valor máximo permitido
            entero: Si True, solo permite enteros
            
        Returns:
            El número ingresado
        """
        while True:
            try:
                valor_str = input(mensaje).strip()
                valor = int(valor_str) if entero else float(valor_str)
                
                if min_val is not None and valor < min_val:
                    print(f"❌ El valor debe ser mayor o igual a {min_val}")
                    continue
                
                if max_val is not None and valor > max_val:
                    print(f"❌ El valor debe ser menor o igual a {max_val}")
                    continue
                
                return valor
            
            except ValueError:
                print(f"❌ Por favor ingrese un número {'entero' if entero else 'válido'}")
    
    def mostrar_producto(self, producto: Producto):
        """Muestra la información de un producto de forma formateada"""
        print(f"\n📖 {producto.nombre}")
        print(f"   ID: {producto.id}")
        print(f"   Autor: {producto.autor}")
        print(f"   Categoría: {producto.categoria}")
        print(f"   Cantidad: {producto.cantidad}")
        print(f"   Precio: ${producto.precio:.2f}")
        if producto.isbn:
            print(f"   ISBN: {producto.isbn}")
        if producto.etiquetas:
            print(f"   Etiquetas: {', '.join(producto.etiquetas)}")
        print(f"   Fecha de creación: {producto.fecha_creacion.strftime('%Y-%m-%d %H:%M')}")
    
    def mostrar_lista_productos(self, productos: List[Producto], titulo: str = "Productos"):
        """Muestra una lista de productos de forma formateada"""
        if not productos:
            print(f"\n❌ No se encontraron {titulo.lower()}")
            return
        
        print(f"\n📋 {titulo} ({len(productos)} encontrados)")
        print("-" * 60)
        
        for i, producto in enumerate(productos, 1):
            stock_status = "✅" if producto.cantidad > 5 else "⚠️" if producto.cantidad > 0 else "❌"
            print(f"{i:2d}. {stock_status} [{producto.id:3d}] {producto.nombre[:40]:40s} - "
                  f"{producto.autor[:20]:20s} (${producto.precio:7.2f}) - "
                  f"Stock: {producto.cantidad:3d}")
    
    def agregar_producto(self):
        """Agrega un nuevo producto al inventario"""
        print("\n📖 AGREGAR NUEVO PRODUCTO")
        print("-" * 40)
        
        try:
            nombre = self.obtener_input("Nombre del libro: ")
            autor = self.obtener_input("Autor del libro: ")
            categoria = self.obtener_input("Categoría: ")
            isbn = self.obtener_input("ISBN (opcional): ", obligatorio=False)
            cantidad = self.obtener_numero("Cantidad en stock: ", min_val=0, entero=True)
            precio = self.obtener_numero("Precio del libro: ", min_val=0)
            
            # Agregar producto
            producto = self.inventario.agregar_producto(
                nombre=nombre,
                cantidad=cantidad,
                precio=precio,
                autor=autor,
                categoria=categoria,
                isbn=isbn
            )
            
            print(f"\n✅ Producto agregado exitosamente:")
            self.mostrar_producto(producto)
            
        except Exception as e:
            print(f"\n❌ Error al agregar producto: {e}")
    
    def eliminar_producto(self):
        """Elimina un producto del inventario"""
        print("\n🗑️ ELIMINAR PRODUCTO")
        print("-" * 40)
        
        try:
            id_producto = self.obtener_numero("ID del producto a eliminar: ", min_val=1, entero=True)
            
            # Buscar producto
            producto = self.inventario.buscar_por_id(id_producto)
            if not producto:
                print(f"\n❌ No se encontró un producto con ID {id_producto}")
                return
            
            # Mostrar producto a eliminar
            print("\n📋 Producto a eliminar:")
            self.mostrar_producto(producto)
            
            # Confirmar eliminación
            confirmacion = input("\n⚠️  ¿Está seguro de eliminar este producto? (S/N): ").strip().upper()
            
            if confirmacion == 'S':
                if self.inventario.eliminar_producto(id_producto):
                    print(f"\n✅ Producto eliminado exitosamente")
                else:
                    print(f"\n❌ Error al eliminar el producto")
            else:
                print("\n❌ Operación cancelada")
                
        except Exception as e:
            print(f"\n❌ Error al eliminar producto: {e}")
    
    def actualizar_producto(self):
        """Actualiza un producto existente"""
        print("\n✏️ ACTUALIZAR PRODUCTO")
        print("-" * 40)
        
        try:
            id_producto = self.obtener_numero("ID del producto a actualizar: ", min_val=1, entero=True)
            
            # Buscar producto
            producto = self.inventario.buscar_por_id(id_producto)
            if not producto:
                print(f"\n❌ No se encontró un producto con ID {id_producto}")
                return
            
            # Mostrar producto actual
            print("\n📋 Producto actual:")
            self.mostrar_producto(producto)
            
            print("\n📝 Ingrese los nuevos valores (deje en blanco para mantener el actual):")
            
            # Obtener nuevos valores
            actualizaciones = {}
            
            nombre = input(f"Nombre [{producto.nombre}]: ").strip()
            if nombre:
                actualizaciones['nombre'] = nombre
            
            autor = input(f"Autor [{producto.autor}]: ").strip()
            if autor:
                actualizaciones['autor'] = autor
            
            categoria = input(f"Categoría [{producto.categoria}]: ").strip()
            if categoria:
                actualizaciones['categoria'] = categoria
            
            isbn = input(f"ISBN [{producto.isbn}]: ").strip()
            if isbn:
                actualizaciones['isbn'] = isbn
            
            cantidad_str = input(f"Cantidad [{producto.cantidad}]: ").strip()
            if cantidad_str:
                try:
                    cantidad = int(cantidad_str)
                    if cantidad >= 0:
                        actualizaciones['cantidad'] = cantidad
                    else:
                        print("⚠️  La cantidad no puede ser negativa, se mantendrá el valor actual")
                except ValueError:
                    print("⚠️  Valor inválido para cantidad, se mantendrá el valor actual")
            
            precio_str = input(f"Precio [{producto.precio}]: ").strip()
            if precio_str:
                try:
                    precio = float(precio_str)
                    if precio >= 0:
                        actualizaciones['precio'] = precio
                    else:
                        print("⚠️  El precio no puede ser negativo, se mantendrá el valor actual")
                except ValueError:
                    print("⚠️  Valor inválido para precio, se mantendrá el valor actual")
            
            if actualizaciones:
                if self.inventario.actualizar_producto(id_producto, **actualizaciones):
                    print(f"\n✅ Producto actualizado exitosamente")
                    # Mostrar producto actualizado
                    producto_actualizado = self.inventario.buscar_por_id(id_producto)
                    if producto_actualizado:
                        self.mostrar_producto(producto_actualizado)
                else:
                    print(f"\n❌ Error al actualizar el producto")
            else:
                print("\nℹ️  No se realizaron cambios")
                
        except Exception as e:
            print(f"\n❌ Error al actualizar producto: {e}")
    
    def buscar_producto(self):
        """Busca productos por diferentes criterios"""
        print("\n🔍 BUSCAR PRODUCTO")
        print("-" * 40)
        print("1. Por nombre")
        print("2. Por ID")
        print("3. Por ISBN")
        print("4. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == '1':
            self.buscar_por_nombre()
        elif opcion == '2':
            self.buscar_por_id()
        elif opcion == '3':
            self.buscar_por_isbn()
        elif opcion == '4':
            return
        else:
            print("❌ Opción inválida")
    
    def buscar_por_nombre(self):
        """Busca productos por nombre"""
        nombre = self.obtener_input("Ingrese el nombre o parte del nombre a buscar: ")
        
        productos = self.inventario.buscar_por_nombre(nombre)
        self.mostrar_lista_productos(productos, f"Resultados para '{nombre}'")
    
    def buscar_por_id(self):
        """Busca un producto por ID"""
        try:
            id_producto = self.obtener_numero("ID del producto: ", min_val=1, entero=True)
            
            producto = self.inventario.buscar_por_id(id_producto)
            if producto:
                print(f"\n✅ Producto encontrado:")
                self.mostrar_producto(producto)
            else:
                print(f"\n❌ No se encontró un producto con ID {id_producto}")
                
        except Exception as e:
            print(f"\n❌ Error al buscar por ID: {e}")
    
    def buscar_por_isbn(self):
        """Busca un producto por ISBN"""
        isbn = self.obtener_input("ISBN a buscar: ")
        
        producto = self.inventario.buscar_por_isbn(isbn)
        if producto:
            print(f"\n✅ Producto encontrado:")
            self.mostrar_producto(producto)
        else:
            print(f"\n❌ No se encontró un producto con ISBN {isbn}")
    
    def buscar_por_categoria(self):
        """Busca productos por categoría"""
        categorias = self.inventario.obtener_categorias()
        
        if not categorias:
            print("\n❌ No hay categorías disponibles")
            return
        
        print("\n📂 Categorías disponibles:")
        for i, categoria in enumerate(categorias, 1):
            print(f"{i}. {categoria}")
        
        try:
            opcion = self.obtener_numero("Seleccione una categoría: ", min_val=1, max_val=len(categorias), entero=True)
            categoria_seleccionada = categorias[opcion - 1]
            
            productos = self.inventario.buscar_por_categoria(categoria_seleccionada)
            self.mostrar_lista_productos(productos, f"Libros de '{categoria_seleccionada}'")
            
        except Exception as e:
            print(f"\n❌ Error al buscar por categoría: {e}")
    
    def buscar_por_autor(self):
        """Busca productos por autor"""
        autores = self.inventario.obtener_autores()
        
        if not autores:
            print("\n❌ No hay autores disponibles")
            return
        
        print("\n👥 Autores disponibles:")
        for i, autor in enumerate(autores, 1):
            print(f"{i}. {autor}")
        
        try:
            opcion = self.obtener_numero("Seleccione un autor: ", min_val=1, max_val=len(autores), entero=True)
            autor_seleccionado = autores[opcion - 1]
            
            productos = self.inventario.buscar_por_autor(autor_seleccionado)
            self.mostrar_lista_productos(productos, f"Libros de '{autor_seleccionado}'")
            
        except Exception as e:
            print(f"\n❌ Error al buscar por autor: {e}")
    
    def mostrar_todos(self):
        """Muestra todos los productos del inventario"""
        productos = self.inventario.obtener_todos()
        self.mostrar_lista_productos(productos, "Todos los productos")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del inventario"""
        print("\n📊 ESTADÍSTICAS DEL INVENTARIO")
        print("-" * 40)
        
        stats = self.inventario.obtener_estadisticas()
        
        print(f"📈 Total de productos: {stats['total_productos']}")
        print(f"📂 Total de categorías: {stats['total_categorias']}")
        print(f"👥 Total de autores: {stats['total_autores']}")
        print(f"💰 Valor total del inventario: ${stats['valor_total_inventario']:,.2f}")
        print(f"📦 Cantidad total de unidades: {stats['cantidad_total']}")
        print(f"💵 Precio promedio por libro: ${stats['precio_promedio']:.2f}")
        
        if stats['categorias_mas_populares']:
            print(f"\n🏆 Categorías más populares:")
            for categoria, count in stats['categorias_mas_populares']:
                print(f"   📚 {categoria}: {count} libros")
        
        if stats['autores_mas_productivos']:
            print(f"\n✍️ Autores más productivos:")
            for autor, count in stats['autores_mas_productivos']:
                print(f"   👤 {autor}: {count} libros")
    
    def mostrar_categorias(self):
        """Muestra todas las categorías disponibles"""
        categorias = self.inventario.obtener_categorias()
        
        if not categorias:
            print("\n❌ No hay categorías disponibles")
            return
        
        print(f"\n📂 Categorías disponibles ({len(categorias)}):")
        print("-" * 40)
        
        for i, categoria in enumerate(categorias, 1):
            productos_categoria = self.inventario.buscar_por_categoria(categoria)
            print(f"{i:2d}. 📚 {categoria} ({len(productos_categoria)} libros)")
    
    def mostrar_autores(self):
        """Muestra todos los autores disponibles"""
        autores = self.inventario.obtener_autores()
        
        if not autores:
            print("\n❌ No hay autores disponibles")
            return
        
        print(f"\n👥 Autores disponibles ({len(autores)}):")
        print("-" * 40)
        
        for i, autor in enumerate(autores, 1):
            productos_autor = self.inventario.buscar_por_autor(autor)
            print(f"{i:2d}. ✍️ {autor} ({len(productos_autor)} libros)")
    
    def productos_bajo_stock(self):
        """Muestra productos con bajo stock"""
        umbral = self.obtener_numero("Umbral de stock bajo (default 5): ", min_val=0, entero=True)
        
        productos = self.inventario.productos_bajo_stock(umbral)
        
        if productos:
            print(f"\n⚠️ PRODUCTOS CON BAJO STOCK (≤ {umbral} unidades)")
            print("-" * 60)
            
            for producto in productos:
                print(f"📖 {producto.nombre}")
                print(f"   ID: {producto.id} | Stock: {producto.cantidad} | Precio: ${producto.precio:.2f}")
                print(f"   Autor: {producto.autor} | Categoría: {producto.categoria}")
                print("-" * 40)
        else:
            print(f"\n✅ No hay productos con stock bajo (≤ {umbral} unidades)")
    
    def exportar_datos(self):
        """Exporta los datos del inventario"""
        print("\n💾 EXPORTAR DATOS")
        print("-" * 40)
        print("1. Exportar como lista de tuplas")
        print("2. Exportar estadísticas")
        print("3. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == '1':
            self.exportar_tuplas()
        elif opcion == '2':
            self.exportar_estadisticas()
        elif opcion == '3':
            return
        else:
            print("❌ Opción inválida")
    
    def exportar_tuplas(self):
        """Exporta el inventario como lista de tuplas"""
        tuplas = self.inventario.exportar_a_lista_tuplas()
        
        print(f"\n📋 INVENTARIO EXPORTADO COMO TUPLAS ({len(tuplas)} productos)")
        print("-" * 80)
        print("Formato: (ID, Nombre, Cantidad, Precio, Autor, Categoría, ISBN)")
        print("-" * 80)
        
        for tupla in tuplas:
            print(f"   {tupla}")
    
    def exportar_estadisticas(self):
        """Exporta las estadísticas del inventario"""
        stats = self.inventario.obtener_estadisticas()
        
        print(f"\n📊 ESTADÍSTICAS EXPORTADAS")
        print("-" * 40)
        
        for clave, valor in stats.items():
            print(f"   {clave}: {valor}")
    
    def salir(self):
        """Sale del programa"""
        print("\n👋 ¡Gracias por usar el Sistema de Gestión de Inventario!")
        print("📚 Librería Virtual - Todos los derechos reservados")
        return False
    
    def ejecutar(self):
        """Ejecuta el menú principal"""
        ejecutando = True
        
        while ejecutando:
            try:
                self.limpiar_pantalla()
                self.mostrar_header()
                self.mostrar_menu_principal()
                
                opcion = input("\nSeleccione una opción: ").strip()
                
                if opcion in self.opciones_menu:
                    resultado = self.opciones_menu[opcion]()
                    
                    if resultado is False:  # Para salir
                        ejecutando = False
                    else:
                        input("\nPresione Enter para continuar...")
                else:
                    print("❌ Opción inválida. Por favor seleccione una opción válida.")
                    input("\nPresione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrumpido. ¡Hasta pronto!")
                ejecutando = False
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                input("\nPresione Enter para continuar...")


def main():
    """Función principal para ejecutar el menú interactivo"""
    menu = MenuInventario()
    menu.ejecutar()


if __name__ == "__main__":
    main()
