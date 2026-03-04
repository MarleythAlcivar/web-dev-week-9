import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import Inventario, Producto
from inventario.inventario import FilePersistence
from inventario.bd import init_db, get_db
from inventario.productos import Producto as ProductoSQLAlchemy
from sqlalchemy.orm import Session

# Configuración simple para caso educativo
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-educativa'

# Inicializar el inventario global
inventario = Inventario()
file_persistence = FilePersistence()

@app.route('/')
def index():
    # Obtener productos destacados para la página principal
    productos = inventario.obtener_todos()
    productos_destacados = productos[:6] if len(productos) >= 6 else productos
    stats = inventario.obtener_estadisticas()
    return render_template('index.html', 
                         productos_destacados=productos_destacados,
                         stats=stats)

@app.route('/about')
def about():
    stats = inventario.obtener_estadisticas()
    return render_template('about.html', stats=stats)

@app.route('/libros')
def libros():
    # Obtener parámetros de filtrado
    categoria = request.args.get('categoria')
    autor = request.args.get('autor')
    busqueda = request.args.get('busqueda')
    
    # Filtrar productos según los parámetros
    if categoria:
        productos = inventario.buscar_por_categoria(categoria)
    elif autor:
        productos = inventario.buscar_por_autor(autor)
    elif busqueda:
        productos = inventario.buscar_por_nombre(busqueda)
    else:
        productos = inventario.obtener_todos()
    
    # Obtener categorías y autores para los filtros
    categorias = inventario.obtener_categorias()
    autores = inventario.obtener_autores()
    
    return render_template('libros.html', 
                         productos=productos,
                         categorias=categorias,
                         autores=autores,
                         categoria_actual=categoria,
                         autor_actual=autor,
                         busqueda_actual=busqueda)

@app.route('/catalogo')
def catalogo():
    productos = inventario.obtener_todos()
    categorias = inventario.obtener_categorias()
    stats = inventario.obtener_estadisticas()
    
    # Agrupar productos por categoría
    productos_por_categoria = {}
    for categoria in categorias:
        productos_por_categoria[categoria] = inventario.buscar_por_categoria(categoria)
    
    return render_template('catalogo.html', 
                         productos=productos,
                         productos_por_categoria=productos_por_categoria,
                         categorias=categorias,
                         stats=stats)

@app.route('/libro/<int:id>')
def libro(id):
    producto = inventario.buscar_por_id(id)
    if producto:
        return render_template('libro_detalle.html', producto=producto)
    else:
        # Si no se encuentra el producto, mostrar página de error
        return render_template('libro_detalle.html', producto=None, error=True)

@app.route('/usuario/<nombre>')
def usuario(nombre):
    # Buscar productos por autor si el nombre coincide con algún autor
    productos_autor = inventario.buscar_por_autor(nombre)
    return render_template('usuario.html', nombre=nombre, productos_autor=productos_autor)

# Rutas API para operaciones CRUD
@app.route('/api/productos', methods=['GET'])
def api_productos():
    productos = inventario.obtener_todos()
    return jsonify([p.a_diccionario() for p in productos])

@app.route('/api/producto', methods=['POST'])
def api_agregar_producto():
    try:
        data = request.get_json()
        producto = inventario.agregar_producto(
            nombre=data['nombre'],
            cantidad=data['cantidad'],
            precio=data['precio'],
            autor=data['autor'],
            categoria=data['categoria'],
            isbn=data.get('isbn', '')
        )
        return jsonify({'success': True, 'producto': producto.a_diccionario()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/producto/<int:id>', methods=['PUT'])
def api_actualizar_producto(id):
    try:
        data = request.get_json()
        exito = inventario.actualizar_producto(id, **data)
        if exito:
            producto = inventario.buscar_por_id(id)
            return jsonify({'success': True, 'producto': producto.a_diccionario()})
        else:
            return jsonify({'success': False, 'error': 'Producto no encontrado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/producto/<int:id>', methods=['DELETE'])
def api_eliminar_producto(id):
    try:
        exito = inventario.eliminar_producto(id)
        return jsonify({'success': exito})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/buscar')
def api_buscar():
    termino = request.args.get('q', '')
    tipo = request.args.get('tipo', 'nombre')  # nombre, autor, categoria, isbn
    
    resultados = []
    if tipo == 'nombre':
        resultados = inventario.buscar_por_nombre(termino)
    elif tipo == 'autor':
        resultados = inventario.buscar_por_autor(termino)
    elif tipo == 'categoria':
        resultados = inventario.buscar_por_categoria(termino)
    elif tipo == 'isbn':
        producto = inventario.buscar_por_isbn(termino)
        if producto:
            resultados = [producto]
    
    return jsonify([p.a_diccionario() for p in resultados])

@app.route('/api/estadisticas')
def api_estadisticas():
    return jsonify(inventario.obtener_estadisticas())

# Rutas de administración para CRUD
@app.route('/admin')
def admin():
    productos = inventario.obtener_todos()
    stats = inventario.obtener_estadisticas()
    return render_template('admin.html', productos=productos, stats=stats)

@app.route('/admin/agregar', methods=['POST'])
def admin_agregar():
    try:
        nombre = request.form['nombre']
        autor = request.form['autor']
        categoria = request.form['categoria']
        isbn = request.form.get('isbn', '')
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        
        producto = inventario.agregar_producto(
            nombre=nombre,
            autor=autor,
            categoria=categoria,
            isbn=isbn,
            cantidad=cantidad,
            precio=precio
        )
        
        return redirect(url_for('admin'))
        
    except Exception as e:
        return f"Error al agregar libro: {e}", 400

@app.route('/admin/editar', methods=['POST'])
def admin_editar():
    try:
        id_producto = int(request.form['id'])
        
        # Obtener solo los campos que fueron enviados
        actualizaciones = {}
        
        if request.form.get('nombre'):
            actualizaciones['nombre'] = request.form['nombre']
        if request.form.get('autor'):
            actualizaciones['autor'] = request.form['autor']
        if request.form.get('categoria'):
            actualizaciones['categoria'] = request.form['categoria']
        if request.form.get('isbn'):
            actualizaciones['isbn'] = request.form['isbn']
        if request.form.get('cantidad'):
            actualizaciones['cantidad'] = int(request.form['cantidad'])
        if request.form.get('precio'):
            actualizaciones['precio'] = float(request.form['precio'])
        
        if inventario.actualizar_producto(id_producto, **actualizaciones):
            return redirect(url_for('admin'))
        else:
            return "No se encontró el libro", 404
            
    except Exception as e:
        return f"Error al editar libro: {e}", 400

@app.route('/admin/eliminar', methods=['POST'])
def admin_eliminar():
    try:
        id_producto = int(request.form['id'])
        
        if inventario.eliminar_producto(id_producto):
            return redirect(url_for('admin'))
        else:
            return "No se encontró el libro", 404
            
    except Exception as e:
        return f"Error al eliminar libro: {e}", 400
            
# Rutas para formularios y productos
@app.route('/productos')
def productos():
    """Página de gestión de productos"""
    productos = inventario.obtener_todos()
    stats = inventario.obtener_estadisticas()
    return render_template('productos.html', productos=productos, stats=stats)

@app.route('/producto/nuevo')
def producto_nuevo():
    """Formulario para nuevo producto"""
    from form import ProductoForm
    form = ProductoForm()
    return render_template('producto_form.html', form=form)

@app.route('/producto/agregar', methods=['POST'])
def agregar_producto():
    """Agregar un nuevo producto"""
    try:
        nombre = request.form['nombre']
        autor = request.form['autor']
        categoria = request.form.get('categoria', '')
        isbn = request.form.get('isbn', '')
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        
        producto = inventario.agregar_producto(
            nombre=nombre,
            autor=autor,
            categoria=categoria,
            isbn=isbn,
            cantidad=cantidad,
            precio=precio
        )
        
        return redirect(url_for('productos'))
        
    except Exception as e:
        return f"Error al agregar producto: {e}", 400

@app.route('/contactos')
def contactos():
    """Página de contactos"""
    return render_template('contactos.html')

# Rutas para persistencia de datos
@app.route('/datos')
def datos():
    """Página principal de gestión de datos"""
    file_info = file_persistence.get_file_info()
    
    # Cargar datos desde diferentes formatos
    txt_data = file_persistence.read_from_txt()
    json_data = file_persistence.read_from_json()
    csv_data = file_persistence.read_from_csv()
    
    # Cargar datos desde SQLite
    sqlite_data = []
    try:
        with Session(app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///inventario_sqlalchemy.db').bind) as session:
            sqlite_data = [producto.to_dict() for producto in session.query(ProductoSQLAlchemy).all()]
    except Exception as e:
        print(f"Error cargando desde SQLite: {e}")
    
    return render_template('datos.html', 
                         file_info=file_info,
                         txt_data=txt_data,
                         json_data=json_data,
                         csv_data=csv_data,
                         sqlite_data=sqlite_data)

@app.route('/datos/save/<format>', methods=['POST'])
def save_data(format):
    """Guardar datos en diferentes formatos"""
    try:
        # Obtener datos del inventario actual
        productos = inventario.obtener_todos()
        data = [producto.a_diccionario() for producto in productos]
        
        success = False
        if format == 'txt':
            success = file_persistence.save_to_txt(data)
        elif format == 'json':
            success = file_persistence.save_to_json(data)
        elif format == 'csv':
            success = file_persistence.save_to_csv(data)
        elif format == 'sqlite':
            success = save_to_sqlalchemy(data)
        
        if success:
            return jsonify({'success': True, 'message': f'Datos guardados en {format.upper()}'})
        else:
            return jsonify({'success': False, 'error': f'Error al guardar en {format.upper()}'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/datos/load/<format>', methods=['GET', 'POST'])
def load_data(format):
    """Cargar datos desde diferentes formatos"""
    try:
        data = []
        
        if format == 'txt':
            data = file_persistence.read_from_txt()
        elif format == 'json':
            data = file_persistence.read_from_json()
        elif format == 'csv':
            data = file_persistence.read_from_csv()
        elif format == 'sqlite':
            data = load_from_sqlalchemy()
        
        # Importar datos al inventario
        imported_count = 0
        for item in data:
            try:
                inventario.agregar_producto(
                    nombre=item.get('nombre', 'Sin nombre'),
                    cantidad=int(item.get('cantidad', 0)),
                    precio=float(item.get('precio', 0)),
                    autor=item.get('autor', 'Sin autor'),
                    categoria=item.get('categoria', 'Sin categoría'),
                    isbn=item.get('isbn', '')
                )
                imported_count += 1
            except Exception as e:
                print(f"Error importando item {item}: {e}")
        
        return jsonify({
            'success': True, 
            'message': f'Se importaron {imported_count} productos desde {format.upper()}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def save_to_sqlalchemy(data):
    """Guardar datos en SQLite usando SQLAlchemy"""
    try:
        # Inicializar la base de datos
        from inventario.bd import engine
        from inventario.productos import Producto as ProductoSQLAlchemy
        from sqlalchemy.orm import Session
        
        # Crear tablas si no existen
        from inventario.bd import Base
        Base.metadata.create_all(bind=engine)
        
        with Session(engine) as session:
            # Limpiar datos existentes (opcional)
            session.query(ProductoSQLAlchemy).delete()
            
            # Insertar nuevos datos
            for item in data:
                producto = ProductoSQLAlchemy(
                    nombre=item.get('nombre'),
                    autor=item.get('autor'),
                    categoria=item.get('categoria'),
                    isbn=item.get('isbn'),
                    cantidad=item.get('cantidad', 0),
                    precio=item.get('precio', 0.0)
                )
                session.add(producto)
            
            session.commit()
        
        return True
    except Exception as e:
        print(f"Error guardando en SQLAlchemy: {e}")
        return False

def load_from_sqlalchemy():
    """Cargar datos desde SQLite usando SQLAlchemy"""
    try:
        from inventario.bd import engine
        from inventario.productos import Producto as ProductoSQLAlchemy
        from sqlalchemy.orm import Session
        
        with Session(engine) as session:
            productos = session.query(ProductoSQLAlchemy).all()
            return [producto.to_dict() for producto in productos]
    except Exception as e:
        print(f"Error cargando desde SQLAlchemy: {e}")
        return []

if __name__ == '__main__':
    # Configuración simple para caso educativo
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
