import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Biblioteca Virtual - Consulta de libros</h1><p>Bienvenido a la Biblioteca Virtual - Tu portal para consulta de libros y recursos académicos.</p>'

@app.route('/libro/<titulo>')
def libro(titulo):
    return f'<h2>Libro: {titulo}</h2><p>Libro: {titulo} - consulta exitosa.</p><a href="/">Volver al inicio</a>'

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'<h2>Bienvenido, {nombre}!</h2><p>¡Hola, {nombre}! Bienvenido a la Biblioteca Virtual.</p><a href="/">Volver al inicio</a>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
