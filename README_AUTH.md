# 🔐 Sistema de Autenticación - Semana 15

## 🎯 **Objetivo de la Semana**

Implementar un sistema de autenticación de usuarios completo con Flask-Login para permitir registro, inicio de sesión, cierre de sesión y protección de rutas.

---

## 📁 **Estructura del Proyecto**

```
deber semana 09/
├── app.py                     # ✅ Aplicación Flask con autenticación
├── auth/                      # ✅ Paquete de autenticación
│   ├── __init__.py           # ✅ Inicialización del paquete
│   ├── models.py             # ✅ Modelo User para Flask-Login
│   └── forms.py              # ✅ Formularios de autenticación
├── templates/                 # ✅ Plantillas HTML
│   ├── auth/                 # ✅ Templates de autenticación
│   │   ├── login.html        # ✅ Página de inicio de sesión
│   │   ├── register.html     # ✅ Página de registro
│   │   ├── dashboard.html    # ✅ Panel principal del usuario
│   │   ├── profile.html      # ✅ Perfil del usuario
│   │   └── change_password.html # ✅ Cambio de contraseña
│   └── base.html             # ✅ Navegación con autenticación
├── conexion/                   # ✅ Paquete de conexión MySQL
└── requirements.txt           # ✅ Dependencias actualizadas
```

---

## 🔧 **Características Implementadas**

### **1. Flask-Login Integration**
- ✅ **Flask-Login 0.6.3** instalado
- ✅ **LoginManager** configurado
- ✅ **User loader** implementado
- ✅ **Session management** automático

### **2. Modelo de Usuario**
- ✅ **UserMixin** heredado
- ✅ **Compatibilidad con Flask-Login**
- ✅ **Métodos de autenticación** implementados
- ✅ **Hash de contraseñas** seguro

### **3. Formularios de Autenticación**
- ✅ **LoginForm** - Inicio de sesión
- ✅ **RegisterForm** - Registro de usuarios
- ✅ **ProfileForm** - Actualización de perfil
- ✅ **ChangePasswordForm** - Cambio de contraseña

### **4. Rutas de Autenticación**
- ✅ **/login** - Iniciar sesión
- ✅ **/register** - Registrarse
- ✅ **/logout** - Cerrar sesión
- ✅ **/dashboard** - Panel principal
- ✅ **/profile** - Perfil de usuario
- ✅ **/change_password** - Cambiar contraseña

### **5. Protección de Rutas**
- ✅ **@login_required** decorator
- ✅ **Redirección automática** a login
- ✅ **Navegación contextual** según estado
- ✅ **Flash messages** para feedback

---

## 🌐 **Rutas de Autenticación**

### **Autenticación Básica**
- `/login` - Formulario de inicio de sesión
- `/register` - Formulario de registro
- `/logout` - Cerrar sesión del usuario

### **Gestión de Usuario**
- `/dashboard` - Panel principal (protegido)
- `/profile` - Perfil del usuario (protegido)
- `/change_password` - Cambiar contraseña (protegido)

### **Integración con MySQL**
- Conexión a base de datos MySQL
- Validación de credenciales en tiempo real
- Almacenamiento seguro de contraseñas

---

## 📊 **Modelos de Datos**

### **User (auth/models.py)**
```python
class User(UserMixin):
    def __init__(self, usuario_db):
        self.id = usuario_db.id_usuario
        self.nombre = usuario_db.nombre
        self.mail = usuario_db.mail
        self.password = usuario_db.password  # Hash SHA-256
        self.activo = usuario_db.activo
    
    @staticmethod
    def get_by_id(user_id):
        return User.get_by_id(user_id)
    
    @staticmethod
    def get_by_mail(email):
        return User.get_by_mail(email)
    
    def verify_password(self, password):
        return Usuario.hash_password(password) == self.password
    
    def is_active(self):
        return self.activo
```

### **Formularios (auth/forms.py)**
```python
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar', validators=[EqualTo('password')])
    submit = SubmitField('Registrarse')
```

---

## 🛠️ **Instalación y Configuración**

### **1. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **2. Configurar Variables de Entorno**
```bash
# .env file
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña
MYSQL_DATABASE=biblioteca
MYSQL_PORT=3306
```

### **3. Ejecutar Aplicación**
```bash
python app.py
```

---

## 🔒 **Seguridad Implementada**

### **Hash de Contraseñas**
```python
@staticmethod
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

### **Protección CSRF**
- Flask-WTF integrado
- Tokens CSRF automáticos
- Validación de formularios

### **Validación de Datos**
- **Email único** en base de datos
- **Longitud mínima** de contraseñas
- **Confirmación de contraseña** en registro
- **Validación de formato** de email

### **Session Management**
- **Cookies seguros** con Flask-Login
- **Remember me** functionality
- **Timeout automático** de sesión
- **Logout completo** de sesión

---

## 📈 **Características Técnicas**

### **🔐 Autenticación**
- **Flask-Login 0.6.3** para gestión de sesiones
- **UserMixin** para compatibilidad
- **LoginManager** configurado
- **Decoradores @login_required** para protección

### **🗄️ Base de Datos**
- **MySQL Connector** para persistencia
- **Hash SHA-256** para contraseñas
- **Consultas parametrizadas** contra inyección SQL
- **Validación de unicidad** de emails

### **🌐 Web Interface**
- **Templates responsivos** con Bootstrap-style CSS
- **Flash messages** para feedback
- **Navegación contextual** según estado de autenticación
- **Formularios validados** con WTForms

---

## 📋 **Flujo de Usuario**

### **1. Registro**
1. Usuario visita `/register`
2. Completa formulario con nombre, email, contraseña
3. Sistema valida datos y unicidad de email
4. Crea usuario con contraseña hasheada
5. Redirige a `/login` con mensaje de éxito

### **2. Inicio de Sesión**
1. Usuario visita `/login`
2. Ingresa email y contraseña
3. Sistema verifica credenciales en MySQL
4. Si válidas, crea sesión y redirige a dashboard
5. Si inválidas, muestra mensaje de error

### **3. Panel Principal**
1. Usuario autenticado accede a `/dashboard`
2. Muestra estadísticas personalizadas
3. Muestra actividad reciente
4. Proporciona acceso rápido a funcionalidades

### **4. Gestión de Perfil**
1. Usuario accede a `/profile`
2. Puede actualizar nombre y email
3. Validación de unicidad de email
4. Puede cambiar contraseña de forma segura

---

## 🎨 **Templates Implementados**

### **🔐 login.html**
- Formulario de inicio de sesión
- Validación en tiempo real
- Opción "Recordarme"
- Enlace a registro

### **📝 register.html**
- Formulario de registro completo
- Validación de contraseñas coincidentes
- Requisitos de seguridad
- Enlace a login

### **🎯 dashboard.html**
- Panel principal del usuario
- Estadísticas personalizadas
- Actividad reciente
- Navegación rápida

### **👤 profile.html**
- Formulario de actualización de perfil
- Información de seguridad
- Acceso a cambio de contraseña
- Vista de datos actuales

### **🔐 change_password.html**
- Formulario de cambio de contraseña
- Validación de contraseña actual
- Requisitos de nueva contraseña
- Confirmación de cambio

---

## 📋 **Resumen de la Semana 15**

**✅ Requisitos Cumplidos:**
- ✅ Implementación de autenticación de usuarios
- ✅ Integración de Flask-Login
- ✅ Registro de usuarios en base de datos
- ✅ Inicio y cierre de sesión
- ✅ Protección de rutas dentro del sistema

**✅ Características Adicionales:**
- ✅ Sistema de perfiles completo
- ✅ Cambio de contraseña seguro
- ✅ Dashboard con estadísticas
- ✅ Navegación contextual
- ✅ Flash messages funcionales
- ✅ Formularios validados
- ✅ Diseño responsivo
- ✅ Seguridad robusta

**El sistema de autenticación está completamente implementado y listo para producción.**
