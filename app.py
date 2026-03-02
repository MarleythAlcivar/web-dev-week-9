import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import Inventario, Producto

# Configuración simple para caso educativo
app = Flask(__name__)

# Inicializar el inventario global
inventario = Inventario()

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

if __name__ == '__main__':
    # Configuración simple para caso educativo
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
