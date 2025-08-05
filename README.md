# BrandFlow 🚀

**BrandFlow** es la solución definitiva para llevar la identidad de tu marca al siguiente nivel. Este proyecto está diseñado para empresas, startups, y emprendedores que buscan una manera única y efectiva de construir y gestionar la marca de su negocio. Desde la creación de un logotipo hasta la construcción de una estrategia de branding sólida, **BrandFlow** se convierte en tu compañero ideal para crear un flujo constante de ideas innovadoras y visualmente impactantes.

---

## 🚀 Descripción

El branding no es solo un logo, es el corazón de tu negocio. **BrandFlow** es una plataforma que combina creatividad, diseño, y estrategias para ayudar a las marcas a definir y fortalecer su identidad. Con **BrandFlow**, las marcas pueden hacer crecer su presencia en el mercado de manera coherente y memorable.

Este proyecto está centrado en ofrecer soluciones de branding que permitan a las marcas no solo destacar visualmente, sino también conectar emocionalmente con su audiencia. Ya sea que estés creando una marca desde cero o redefiniendo una existente, **BrandFlow** es la herramienta perfecta para transformar tu visión en una experiencia visual impactante.

---

## 🔑 Características

- **Diseño de Marca Personalizado:** Crea una identidad única para tu marca, desde el logotipo hasta las paletas de colores, tipografía y más.
- **Estrategias de Branding:** Desarrolla una estrategia de branding coherente que refleje los valores y la misión de tu empresa.
- **Interfaz Intuitiva:** Interfaz de usuario amigable que permite a los usuarios sin experiencia en diseño crear una marca profesional y bien estructurada.
- **Asesoría Personalizada:** Consultoría en línea con expertos en branding para guiar a tu empresa a través del proceso creativo y estratégico.
- **Optimización Multicanal:** Herramientas para adaptar tu branding a diferentes plataformas y formatos, desde redes sociales hasta materiales impresos.
- **Sistema de Autenticación Robusto:** Gestión completa de usuarios con roles, sesiones seguras y cookies optimizadas.
- **API RESTful:** Interfaz de programación completa para integración con frontend y aplicaciones móviles.

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 4.2.20
- **API:** Django REST Framework
- **Autenticación:** Session Authentication + JWT
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Documentación API:** drf-spectacular
- **Gestión de Sesiones:** Django Sessions con cookies seguras

---

## 🔐 Sistema de Autenticación y Usuarios

### Roles de Usuario
- **Administrador:** Acceso completo al sistema
- **Cliente:** Usuario final con acceso a productos y compras
- **Vendedor:** Gestión de ventas y productos
- **Gerente:** Supervisión y gestión de equipos

### Funcionalidades de Autenticación
- ✅ **Registro de Usuarios:** Creación de cuentas con validación
- ✅ **Login/Logout:** Gestión de sesiones seguras
- ✅ **Perfil de Usuario:** Edición y visualización de datos personales
- ✅ **Gestión de Sesiones:** Cookies seguras con configuración optimizada
- ✅ **Permisos Granulares:** Control de acceso basado en roles
- ✅ **Middleware Personalizado:** Manejo de CSRF y sesiones

### Endpoints de Autenticación
```
POST /api/user/register/     # Registro de usuarios
POST /api/user/login/        # Inicio de sesión
POST /api/user/logout/       # Cierre de sesión
GET  /api/user/profile/      # Perfil del usuario
PUT  /api/user/profile/      # Actualizar perfil
GET  /api/user/session-status/ # Estado de la sesión
```

---

## 🗄️ Arquitectura de Base de Datos

### 🔗 Relaciones entre Modelos

#### 🧑 Usuario (`user_control.Users`)
- **Herencia:** `AbstractUser` de Django
- **Campos adicionales:** `phone`, `address`, `roles`, `company`
- **Relación:** Self-referential ForeignKey para jerarquía empresarial
- **Roles:** admin, cliente, vendedor, gerente
- **Relaciones:**
  - Tiene un **Carrito** (relación uno a uno)
  - Puede realizar múltiples **Pedidos**
  - Puede escribir múltiples **Reseñas**
  - Puede ser **empleado** de otro usuario (empresa)

#### 🛒 Carrito (`brand_control.ShoppCart`)
- **Pertenece a:** Un **Usuario**
- **Contiene:** Múltiples **Detalle_Carrito**
- **Funcionalidad:** Gestión temporal de productos antes de compra

#### 📦 Detalle_Carrito (`brand_control.ShoppCartDetails`)
- **Pertenece a:** Un **Carrito**
- **Asociado a:** Un único **Producto**
- **Campos:** `quantity` (cantidad del producto)

#### 🎨 Producto (`brand_control.Product`)
- **Pertenece a:** Una **Categoría**
- **Relaciones:**
  - Puede estar en múltiples **Detalle_Carrito**
  - Puede estar en múltiples **Detalle_Pedido**
  - Puede tener múltiples **Reseñas**

#### 🗂️ Categoría (`brand_control.Category`)
- **Contiene:** Múltiples **Productos**
- **Funcionalidad:** Organización jerárquica de productos

#### 🧾 Pedido (`brand_control.Order`)
- **Pertenece a:** Un **Usuario**
- **Contiene:** Múltiples **Detalle_Pedido**
- **Tiene:** Un único **Pago** asociado
- **Campos:** `order_date`, `total_amount`, `status`

#### 🧮 Detalle_Pedido (`brand_control.OrderDetails`)
- **Pertenece a:** Un **Pedido**
- **Asociado a:** Un único **Producto**
- **Campos:** `quantity`, `unit_price` (precio al momento del pedido)

#### 💳 Pago (`brand_control.Payment`)
- **Pertenece a:** Un único **Pedido**
- **Campos:** `method`, `status`, `amount`
- **Funcionalidad:** Gestión de transacciones

#### 📝 Reseña (`brand_control.Reviews`)
- **Asociada a:** Un **Usuario** y un **Producto**
- **Campos:** `rating`, `comment`, `created_at`

#### 🏢 Sucursal (`brand_control.Branch`)
- **Pertenece a:** Una **Empresa** (Usuario con rol admin)
- **Funcionalidad:** Gestión de ubicaciones físicas

#### 📊 Movimiento de Stock (`brand_control.StockMovement`)
- **Asociado a:** Un **Producto** y una **Sucursal**
- **Funcionalidad:** Control de inventario

---

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip
- virtualenv (recomendado)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Menguitahh/BrandFlow.git
cd BrandFlow
```

2. **Crear entorno virtual**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Crear usuario de prueba (opcional)**
```bash
python manage.py create_test_user --username testuser --email test@example.com --password Test123!
```

7. **Ejecutar servidor**
```bash
python manage.py runserver
```

### Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
```env
DEBUG=True
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=sqlite:///db.sqlite3
```

---

## 📚 Documentación de la API

### Autenticación
El sistema utiliza autenticación por sesiones con JWT como respaldo:

```python
# Configuración en settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Ejemplos de Uso

#### Registro de Usuario
```bash
curl -X POST http://localhost:8000/api/user/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_usuario",
    "email": "usuario@example.com",
    "password": "Password123!",
    "password2": "Password123!",
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone": "123456789",
    "address": "Calle Principal 123",
    "roles": "cliente"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/user/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "nuevo_usuario",
    "password": "Password123!"
  }'
```

#### Obtener Perfil
```bash
curl -X GET http://localhost:8000/api/user/profile/ \
  -H "Cookie: sessionid=tu_session_id"
```

---

## 🔧 Configuración de Sesiones y Cookies

### Configuración Optimizada para Desarrollo
```python
# settings.py
SESSION_COOKIE_SECURE = False  # True en producción
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
CSRF_COOKIE_SECURE = False  # True en producción
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
```

### Middleware Personalizado
- **SessionMiddleware:** Gestión automática de sesiones
- **CSRFMiddleware:** Exención selectiva de CSRF para endpoints de autenticación

---

## 🧪 Testing

### Comandos de Prueba
```bash
# Ejecutar tests
python manage.py test

# Crear usuario de prueba
python manage.py create_test_user

# Verificar estado del sistema
python manage.py check
```

### Datos de Prueba
```json
{
  "username": "testuser",
  "email": "test@example.com", 
  "password": "Test123!",
  "roles": "cliente"
}
```

---

## 📁 Estructura del Proyecto

```
BrandFlow/
├── BrandFlow/                 # Configuración principal
│   ├── settings.py           # Configuración del proyecto
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # Configuración WSGI
├── user_control/             # App de gestión de usuarios
│   ├── models.py            # Modelo Users
│   ├── views.py             # Vistas de autenticación
│   ├── serializer.py        # Serializers de usuario
│   ├── permissions.py       # Permisos personalizados
│   ├── middleware.py        # Middleware personalizado
│   └── management/          # Comandos de gestión
├── brand_control/           # App de gestión de productos
│   ├── models.py            # Modelos de productos
│   ├── views.py             # Vistas de productos
│   └── serializer.py        # Serializers de productos
├── manage.py                # Script de gestión Django
└── README.md               # Este archivo
```

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 📞 Contacto

- **Desarrollador:** [Tu Nombre]
- **Email:** [tu-email@example.com]
- **Proyecto:** [https://github.com/Menguitahh/BrandFlow](https://github.com/Menguitahh/BrandFlow)

---

## 🎯 Roadmap

- [ ] Implementación de frontend con React/Vue.js
- [ ] Sistema de notificaciones en tiempo real
- [ ] Integración con pasarelas de pago
- [ ] Dashboard administrativo avanzado
- [ ] API para aplicaciones móviles
- [ ] Sistema de reportes y analytics
- [ ] Integración con redes sociales
- [ ] Sistema de recomendaciones de productos

---

**¡Gracias por usar BrandFlow! 🚀**
