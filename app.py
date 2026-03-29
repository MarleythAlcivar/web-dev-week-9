import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, Response, session, flash, send_file
from datetime import datetime
from models import Inventario, Producto
from inventario.inventario import FilePersistence
from inventario.bd import init_db
from inventario.productos import Producto as ProductoSQLAlchemy
from sqlalchemy.orm import Session
from conexion.conexion import get_db_connection
from conexion.models import Usuario, ProductoMySQL, Categoria, Prestamo
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from auth.models import User
from auth.forms import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm
from models.producto import Producto
from services.producto_service import ProductoService
from forms.producto_form import ProductoForm, SearchForm, CategoryFilterForm, StockUpdateForm, DeleteForm
from reports.pdf_generator import PDFGenerator

# Configuración simple para caso educativo
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-educativa'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

# Inicializar el inventario global
inventario = Inventario()
file_persistence = FilePersistence()

# Inicializar base de datos SQLite al iniciar
try:
    init_db()
    print("Base de datos SQLite inicializada")
except Exception as e:
    print(f"Error inicializando base de datos: {e}")

# Inicializar conexión MySQL
try:
    db_mysql = get_db_connection()
    print("Conexión MySQL establecida")
except Exception as e:
    print(f"Error conectando a MySQL: {e}")
    print("Asegúrate de tener MySQL instalado y configurado")

# User loader para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

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
        from inventario.bd import engine
        with Session(engine) as session:
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
        from inventario.bd import engine, Base
        from inventario.productos import Producto as ProductoSQLAlchemy
        from sqlalchemy.orm import Session
        
        # Crear tablas si no existen
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

# Rutas para descarga de archivos
@app.route('/download/<format>')
def download_file(format):
    """Descargar archivo de datos en formato específico"""
    try:
        content = file_persistence.get_file_content(format)
        
        if not content:
            return "Archivo no encontrado", 404
        
        # Configurar headers para descarga
        if format == 'txt':
            filename = f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            mimetype = 'text/plain'
        elif format == 'json':
            filename = f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            mimetype = 'application/json'
        elif format == 'csv':
            filename = f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            mimetype = 'text/csv'
        else:
            return "Formato no soportado", 400
        
        response = Response(content, mimetype=mimetype)
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        return f"Error al descargar archivo: {e}", 500

# Rutas para MySQL
@app.route('/mysql/setup')
def mysql_setup():
    """Configurar base de datos MySQL"""
    try:
        db = get_db_connection()
        tables_created = db.create_tables()
        
        if len(tables_created) > 0:
            db.insert_sample_data()
            message = f"✅ Base de datos MySQL configurada exitosamente. Tablas creadas: {', '.join(tables_created)}"
        else:
            message = "❌ Error al crear tablas en MySQL"
            
        return render_template('mysql_status.html', message=message, success=len(tables_created) > 0)
        
    except Exception as e:
        return render_template('mysql_status.html', message=f"❌ Error configurando MySQL: {e}", success=False)

@app.route('/mysql/usuarios')
def mysql_usuarios():
    """Gestión de usuarios en MySQL"""
    try:
        usuarios = Usuario.get_all()
        return render_template('mysql_usuarios.html', usuarios=usuarios)
    except Exception as e:
        return f"Error cargando usuarios: {e}", 500

@app.route('/mysql/usuarios/nuevo', methods=['GET', 'POST'])
def mysql_usuario_nuevo():
    """Crear nuevo usuario en MySQL"""
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            mail = request.form['mail']
            password = request.form['password']
            
            usuario = Usuario(nombre=nombre, mail=mail, password=password)
            
            if usuario.create():
                flash('✅ Usuario creado exitosamente', 'success')
                return redirect(url_for('mysql_usuarios'))
            else:
                flash('❌ Error al crear usuario', 'error')
                
        except Exception as e:
            flash(f'❌ Error: {e}', 'error')
    
    return render_template('mysql_usuario_form.html', action='Crear')

@app.route('/mysql/usuarios/editar/<int:id_usuario>', methods=['GET', 'POST'])
def mysql_usuario_editar(id_usuario):
    """Editar usuario en MySQL"""
    usuario = Usuario.get_by_id(id_usuario)
    
    if not usuario:
        flash('❌ Usuario no encontrado', 'error')
        return redirect(url_for('mysql_usuarios'))
    
    if request.method == 'POST':
        try:
            usuario.nombre = request.form['nombre']
            usuario.mail = request.form['mail']
            usuario.activo = 'activo' in request.form
            
            if usuario.update():
                flash('✅ Usuario actualizado exitosamente', 'success')
                return redirect(url_for('mysql_usuarios'))
            else:
                flash('❌ Error al actualizar usuario', 'error')
                
        except Exception as e:
            flash(f'❌ Error: {e}', 'error')
    
    return render_template('mysql_usuario_form.html', usuario=usuario, action='Editar')

@app.route('/mysql/usuarios/eliminar/<int:id_usuario>')
def mysql_usuario_eliminar(id_usuario):
    """Eliminar usuario en MySQL"""
    try:
        usuario = Usuario.get_by_id(id_usuario)
        
        if usuario and usuario.delete():
            flash('✅ Usuario eliminado exitosamente', 'success')
        else:
            flash('❌ Error al eliminar usuario', 'error')
            
    except Exception as e:
        flash(f'❌ Error: {e}', 'error')
    
    return redirect(url_for('mysql_usuarios'))

@app.route('/mysql/productos')
def mysql_productos():
    """Gestión de productos en MySQL"""
    try:
        productos = ProductoMySQL.get_all()
        categorias = Categoria.get_all()
        return render_template('mysql_productos.html', productos=productos, categorias=categorias)
    except Exception as e:
        return f"Error cargando productos: {e}", 500

@app.route('/mysql/productos/nuevo', methods=['GET', 'POST'])
def mysql_producto_nuevo():
    """Crear nuevo producto en MySQL"""
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            autor = request.form['autor']
            categoria = request.form['categoria']
            isbn = request.form['isbn']
            cantidad = int(request.form['cantidad'])
            precio = float(request.form['precio'])
            
            producto = ProductoMySQL(
                nombre=nombre, autor=autor, categoria=categoria,
                isbn=isbn, cantidad=cantidad, precio=precio
            )
            
            if producto.create():
                flash('✅ Producto creado exitosamente', 'success')
                return redirect(url_for('mysql_productos'))
            else:
                flash('❌ Error al crear producto', 'error')
                
        except Exception as e:
            flash(f'❌ Error: {e}', 'error')
    
    categorias = Categoria.get_all()
    return render_template('mysql_producto_form.html', categorias=categorias, action='Crear')

@app.route('/mysql/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
def mysql_producto_editar(id_producto):
    """Editar producto en MySQL"""
    producto = ProductoMySQL.get_by_id(id_producto)
    
    if not producto:
        flash('❌ Producto no encontrado', 'error')
        return redirect(url_for('mysql_productos'))
    
    if request.method == 'POST':
        try:
            producto.nombre = request.form['nombre']
            producto.autor = request.form['autor']
            producto.categoria = request.form['categoria']
            producto.isbn = request.form['isbn']
            producto.cantidad = int(request.form['cantidad'])
            producto.precio = float(request.form['precio'])
            
            if producto.update():
                flash('✅ Producto actualizado exitosamente', 'success')
                return redirect(url_for('mysql_productos'))
            else:
                flash('❌ Error al actualizar producto', 'error')
                
        except Exception as e:
            flash(f'❌ Error: {e}', 'error')
    
    categorias = Categoria.get_all()
    return render_template('mysql_producto_form.html', producto=producto, categorias=categorias, action='Editar')

@app.route('/mysql/productos/eliminar/<int:id_producto>')
def mysql_producto_eliminar(id_producto):
    """Eliminar producto en MySQL"""
    try:
        producto = ProductoMySQL.get_by_id(id_producto)
        
        if producto and producto.delete():
            flash('✅ Producto eliminado exitosamente', 'success')
        else:
            flash('❌ Error al eliminar producto', 'error')
            
    except Exception as e:
        flash(f'❌ Error: {e}', 'error')
    
    return redirect(url_for('mysql_productos'))

@app.route('/mysql/prestamos')
def mysql_prestamos():
    """Gestión de préstamos en MySQL"""
    try:
        prestamos = Prestamo.get_activos()
        usuarios = Usuario.get_all()
        productos = ProductoMySQL.get_all()
        return render_template('mysql_prestamos.html', prestamos=prestamos, usuarios=usuarios, productos=productos)
    except Exception as e:
        return f"Error cargando préstamos: {e}", 500

@app.route('/mysql/prestamos/nuevo', methods=['POST'])
def mysql_prestamo_nuevo():
    """Crear nuevo préstamo en MySQL"""
    try:
        id_usuario = int(request.form['id_usuario'])
        id_producto = int(request.form['id_producto'])
        
        prestamo = Prestamo(id_usuario=id_usuario, id_producto=id_producto)
        
        if prestamo.create():
            flash('✅ Préstamo creado exitosamente', 'success')
        else:
            flash('❌ Error al crear préstamo', 'error')
            
    except Exception as e:
        flash(f'❌ Error: {e}', 'error')
    
    return redirect(url_for('mysql_prestamos'))

@app.route('/mysql/prestamos/devolver/<int:id_prestamo>')
def mysql_prestamo_devolver(id_prestamo):
    """Devolver producto en MySQL"""
    try:
        prestamo = Prestamo(id_prestamo=id_prestamo)
        
        if prestamo.devolver():
            flash('✅ Préstamo devuelto exitosamente', 'success')
        else:
            flash('❌ Error al devolver préstamo', 'error')
            
    except Exception as e:
        flash(f'❌ Error: {e}', 'error')
    
    return redirect(url_for('mysql_prestamos'))

# Rutas del Sistema CRUD
@app.route('/productos', methods=['GET'])
@login_required
def productos_index():
    """Página principal de productos con filtros y búsqueda"""
    page = request.args.get('page', 1, type=int)
    search_term = request.args.get('search', '')
    categoria = request.args.get('categoria', '')
    
    # Crear formularios
    search_form = SearchForm()
    category_form = CategoryFilterForm()
    
    # Obtener productos
    if search_term:
        result = ProductoService.search_products(search_term)
        productos = result['data'] if result['success'] else []
    elif categoria:
        result = ProductoService.get_products_by_category(categoria)
        productos = result['data'] if result['success'] else []
    else:
        result = ProductoService.get_all_products()
        productos = result['data'] if result['success'] else []
    
    # Obtener estadísticas
    stats_result = ProductoService.get_statistics()
    stats = stats_result['data'] if stats_result['success'] else {}
    
    # Paginación simple
    per_page = 10
    total_items = len(productos)
    total_pages = (total_items + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    productos_page = productos[start:end]
    
    return render_template('productos/index.html',
                         productos=productos_page,
                         stats=stats,
                         search_form=search_form,
                         category_form=category_form,
                         current_page=page,
                         total_pages=total_pages,
                         total_items=total_items)

@app.route('/productos/create', methods=['GET', 'POST'])
@login_required
def producto_create():
    """Crear nuevo producto"""
    form = ProductoForm()
    
    if form.validate_on_submit():
        result = ProductoService.create_product(
            form.nombre.data,
            form.descripcion.data,
            form.precio.data,
            form.stock.data,
            form.categoria.data
        )
        
        if result['success']:
            flash(f'✅ {result["message"]}', 'success')
            return redirect(url_for('productos_index'))
        else:
            flash(f'❌ {result["message"]}', 'danger')
    
    return render_template('productos/create.html', form=form)

@app.route('/productos/view/<int:id>', methods=['GET'])
@login_required
def producto_view(id):
    """Ver detalles de un producto"""
    result = ProductoService.get_product_by_id(id)
    
    if result['success']:
        return render_template('productos/view.html', producto=result['data'])
    else:
        flash(f'❌ {result["message"]}', 'danger')
        return redirect(url_for('productos_index'))

@app.route('/productos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def producto_edit(id):
    """Editar producto existente"""
    # Obtener producto actual
    result = ProductoService.get_product_by_id(id)
    
    if not result['success']:
        flash(f'❌ {result["message"]}', 'danger')
        return redirect(url_for('productos_index'))
    
    producto = result['data']
    
    form = ProductoForm()
    
    if request.method == 'GET':
        # Cargar datos actuales en el formulario
        form.nombre.data = producto['nombre']
        form.descripcion.data = producto['descripcion']
        form.precio.data = producto['precio']
        form.stock.data = producto['stock']
        form.categoria.data = producto['categoria']
        form.activo.data = producto['activo']
    
    if form.validate_on_submit():
        result = ProductoService.update_product(
            id,
            form.nombre.data,
            form.descripcion.data,
            form.precio.data,
            form.stock.data,
            form.categoria.data,
            form.activo.data
        )
        
        if result['success']:
            flash(f'✅ {result["message"]}', 'success')
            return redirect(url_for('productos_index'))
        else:
            flash(f'❌ {result["message"]}', 'danger')
    
    return render_template('productos/edit.html', form=form, producto=producto)

@app.route('/productos/delete/<int:id>', methods=['POST'])
@login_required
def producto_delete(id):
    """Eliminar producto"""
    result = ProductoService.delete_product(id)
    
    if result['success']:
        flash(f'✅ {result["message"]}', 'success')
    else:
        flash(f'❌ {result["message"]}', 'danger')
    
    return redirect(url_for('productos_index'))

@app.route('/productos/update-stock/<int:id>', methods=['POST'])
@login_required
def producto_update_stock(id):
    """Actualizar stock de un producto"""
    stock = request.form.get('stock', type=int)
    
    result = ProductoService.update_stock(id, stock)
    
    if result['success']:
        flash(f'✅ {result["message"]}', 'success')
    else:
        flash(f'❌ {result["message"]}', 'danger')
    
    return redirect(url_for('producto_view', id=id))

@app.route('/productos/report', methods=['GET'])
@login_required
def producto_report():
    """Generar reporte PDF de productos"""
    try:
        # Obtener todos los productos
        result = ProductoService.get_all_products()
        productos = result['data'] if result['success'] else []
        
        if not productos:
            flash('❌ No hay productos para generar el reporte', 'warning')
            return redirect(url_for('productos_index'))
        
        # Generar PDF
        pdf_generator = PDFGenerator(f"productos_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        pdf_result = pdf_generator.generate_product_report(productos)
        
        if pdf_result['success']:
            # Enviar archivo al usuario
            return send_file(
                pdf_result['filepath'],
                as_attachment=True,
                download_name=pdf_result['filename'],
                mimetype='application/pdf'
            )
        else:
            flash(f'❌ {pdf_result["message"]}', 'danger')
            return redirect(url_for('productos_index'))
    
    except Exception as e:
        flash(f'❌ Error al generar reporte: {str(e)}', 'danger')
        return redirect(url_for('productos_index'))

@app.route('/productos/low-stock-report', methods=['GET'])
@login_required
def producto_low_stock_report():
    """Generar reporte PDF de productos con bajo stock"""
    try:
        # Obtener productos con bajo stock
        result = ProductoService.get_low_stock_products()
        productos = result['data'] if result['success'] else []
        
        if not productos:
            flash('✅ No hay productos con bajo stock', 'success')
            return redirect(url_for('productos_index'))
        
        # Generar PDF
        pdf_generator = PDFGenerator(f"low_stock_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        pdf_result = pdf_generator.generate_low_stock_report(productos)
        
        if pdf_result['success']:
            # Enviar archivo al usuario
            return send_file(
                pdf_result['filepath'],
                as_attachment=True,
                download_name=pdf_result['filename'],
                mimetype='application/pdf'
            )
        else:
            flash(f'❌ {pdf_result["message"]}', 'danger')
            return redirect(url_for('productos_index'))
    
    except Exception as e:
        flash(f'❌ Error al generar reporte de bajo stock: {str(e)}', 'danger')
        return redirect(url_for('productos_index'))

# Rutas de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.get_by_mail(form.email.data)
        
        if user and user.verify_password(form.password.data):
            if user.is_active():
                login_user(user, remember=form.remember_me.data)
                flash(f'Bienvenido de nuevo, {user.nombre}!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard'))
            else:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'warning')
        else:
            flash('Email o contraseña incorrectos.', 'danger')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Verificar si el email ya existe
        existing_user = User.get_by_mail(form.email.data)
        if existing_user:
            flash('Este email ya está registrado. Usa otro email o inicia sesión.', 'warning')
            return render_template('auth/register.html', form=form)
        
        # Crear nuevo usuario
        usuario_db = Usuario(
            nombre=form.nombre.data,
            mail=form.email.data,
            password=form.password.data
        )
        
        if usuario_db.create():
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error al registrar el usuario. Intenta nuevamente.', 'danger')
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión del usuario"""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Panel principal del usuario autenticado"""
    # Obtener estadísticas del usuario
    try:
        prestamos = Prestamo.get_by_usuario(current_user.id)
        productos_mysql = ProductoMySQL.get_all()
        usuarios = Usuario.get_all()
        
        # Estadísticas
        stats = {
            'total_prestamos': len(prestamos),
            'prestamos_activos': len([p for p in prestamos if p['estado'] == 'activo']),
            'total_productos': len(productos_mysql),
            'total_usuarios': len(usuarios)
        }
        
        return render_template('auth/dashboard.html', 
                         prestamos=prestamos[:5],  # Últimos 5 préstamos
                         stats=stats)
    
    except Exception as e:
        flash(f'Error cargando el dashboard: {e}', 'danger')
        return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Perfil del usuario"""
    form = ProfileForm()
    
    if request.method == 'GET':
        form.nombre.data = current_user.nombre
        form.email.data = current_user.mail
    
    if form.validate_on_submit():
        # Verificar si el email ya existe (y no es el del usuario actual)
        existing_user = User.get_by_mail(form.email.data)
        if existing_user and existing_user.id != current_user.id:
            flash('Este email ya está en uso por otro usuario.', 'warning')
            return render_template('auth/profile.html', form=form)
        
        # Actualizar usuario en la base de datos
        usuario_db = Usuario.get_by_id(current_user.id)
        usuario_db.nombre = form.nombre.data
        usuario_db.mail = form.email.data
        
        if usuario_db.update():
            # Actualizar objeto current_user
            current_user.nombre = form.nombre.data
            current_user.mail = form.email.data
            flash('Perfil actualizado exitosamente.', 'success')
        else:
            flash('Error al actualizar el perfil.', 'danger')
    
    return render_template('auth/profile.html', form=form)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Cambiar contraseña del usuario"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Verificar contraseña actual
        usuario_db = Usuario.get_by_id(current_user.id)
        if usuario_db.verify_password(form.current_password.data):
            # Actualizar contraseña
            usuario_db.password = form.new_password.data
            if usuario_db.update():
                flash('Contraseña cambiada exitosamente.', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Error al cambiar la contraseña.', 'danger')
        else:
            flash('La contraseña actual es incorrecta.', 'danger')
    
    return render_template('auth/change_password.html', form=form)

if __name__ == '__main__':
    # Configuración simple para caso educativo
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
