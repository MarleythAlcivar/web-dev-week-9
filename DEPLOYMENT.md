# Guía de Despliegue - Sistema de Gestión de Inventario

## 🚀 Despliegue en Render

### Requisitos Previos

1. **Cuenta en Render**: https://render.com/
2. **Repositorio Git**: El proyecto debe estar en GitHub/GitLab
3. **Python 3.7+**: Compatible con el runtime de Render

### 📋 Configuración del Proyecto

#### 1. Archivos de Configuración

✅ **`render.yaml`** - Configuración del servicio
✅ **`requirements.txt`** - Dependencias Python
✅ **`.gitignore`** - Archivos excluidos del repo
✅ **`app.py`** - Aplicación Flask principal
✅ **`models.py`** - Clases POO y lógica de negocio

#### 2. Variables de Entorno

Render configurará automáticamente:
- `FLASK_ENV=production`
- `PORT=10000`
- `SECRET_KEY` (generado automáticamente)

### 🔧 Pasos para Despliegue

#### 1. Conectar Repositorio

```bash
# 1. Subir el código a GitHub
git add .
git commit -m "Sistema de gestión de inventario listo para producción"
git push origin main
```

#### 2. Crear Servicio en Render

1. Iniciar sesión en [Render](https://render.com/)
2. Click **"New +"** → **"Web Service"**
3. Conectar el repositorio GitHub
4. Configurar:
   - **Name**: `biblioteca-virtual`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

#### 3. Variables de Entorno

Añadir las siguientes variables de entorno:

```bash
FLASK_ENV=production
PORT=10000
SECRET_KEY=[generado automáticamente]
```

#### 4. Configuración Adicional

- **Health Check Path**: `/`
- **Auto-Deploy**: Activado
- **Plan**: Free (suficiente para demostración)

### 📊 Estructura del Proyecto

```
deber semana 09/
├── app.py                 # Aplicación Flask principal
├── models.py              # Clases POO (Producto, Inventario)
├── menu_interactivo.py    # Interfaz de consola (opcional)
├── demo.py               # Script de demostración (opcional)
├── requirements.txt       # Dependencias Python
├── render.yaml           # Configuración de Render
├── .gitignore            # Archivos excluidos
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── libros.html
│   ├── catalogo.html
│   ├── libro_detalle.html
│   ├── usuario.html
│   ├── admin.html
│   └── error.html
├── static/               # Archivos estáticos (CSS, JS)
└── README.md             # Documentación del proyecto
```

### 🔍 Verificación del Despliegue

#### 1. Health Check

La aplicación responderá con status 200 en:
- `https://[tu-app].onrender.com/`

#### 2. Funcionalidades Críticas

✅ **Página Principal**: Mostrar libros destacados
✅ **Catálogo**: Listado completo de libros
✅ **Búsqueda**: Funcionalidad de búsqueda y filtros
✅ **Detalles**: Vista individual de libros
✅ **Administración**: Panel CRUD completo
✅ **API**: Endpoints REST funcionales

#### 3. Pruebas Post-Despliegue

```bash
# Test de salud
curl https://[tu-app].onrender.com/

# Test de API
curl https://[tu-app].onrender.com/api/productos

# Test de administración
curl https://[tu-app].onrender.com/admin
```

### ⚠️ Consideraciones de Producción

#### 1. Base de Datos

- **SQLite**: Almacenamiento local (persiste entre reinicios)
- **Backup**: Render no hace backup automático de archivos locales
- **Escalabilidad**: Para producción masiva, considerar PostgreSQL

#### 2. Rendimiento

- **Memoria**: El inventario carga todos los productos en memoria
- **Concurrencia**: SQLite maneja bien lecturas concurrentes
- **Cache**: Los índices en memoria optimizan búsquedas

#### 3. Seguridad

- **SECRET_KEY**: Configurado y generado automáticamente
- **Validación**: Inputs validados en el backend
- **Errores**: Manejo adecuado de errores 404/500

### 🐛 Troubleshooting

#### Error Comunes

1. **Build Failed**
   - Verificar `requirements.txt`
   - Revisar sintaxis de Python

2. **Service Not Starting**
   - Verificar `startCommand`
   - Revisar logs de errores

3. **Database Issues**
   - Permisos de escritura en el directorio
   - Path correcto de la base de datos

#### Logs y Monitoreo

Render proporciona:
- **Build Logs**: Durante el despliegue
- **Service Logs**: Runtime de la aplicación
- **Metrics**: CPU, memoria, requests

### 🔄 Actualizaciones

#### Auto-Deploy

Activado por defecto. Cada push a main:
1. Trigger nuevo build
2. Deploy automático
3. Zero downtime (si no hay errores)

#### Manual Deploy

1. Push a rama diferente
2. Manual deploy desde dashboard
3. Rollback si es necesario

### 📈 Escalabilidad

#### Plan Free (Actual)

- **CPU**: 0.25 vCPU shared
- **RAM**: 512MB
- **Bandwidth**: 100GB/mes
- **Sleep**: 15 min inactividad

#### Plan Starter (Recomendado)

- **CPU**: 0.5 vCPU shared  
- **RAM**: 1GB
- **Bandwidth**: 500GB/mes
- **No Sleep**: Siempre activo

### 🎯 Checklist Pre-Despliegue

- [ ] Código en repositorio Git
- [ ] `requirements.txt` actualizado
- [ ] `render.yaml` configurado
- [ ] Variables de entorno definidas
- [ ] Tests locales funcionando
- [ ] Base de datos inicializada
- [ ] Manejo de errores implementado
- [ ] Health check configurado

### 🚀 Comando Final

```bash
# Desplegar en Render
git push origin main
```

El sistema estará disponible en:
`https://biblioteca-virtual.onrender.com`

---

**Soporte**: Revisar logs en Render dashboard para cualquier issue.
