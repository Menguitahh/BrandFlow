# 🎯 **INSTRUCCIONES PARA FRONTEND - PANEL DE ADMIN**

## 📋 **RESUMEN**
El backend está completamente funcional. Aquí tienes todo lo que necesitas para implementar el panel de administración en el frontend.

---

## 🔑 **CREDENCIALES DE ADMIN**
```javascript
const ADMIN_CREDENTIALS = {
  username: "admin",
  password: "Admin123!",
  email: "admin@example.com"
}
```

---

## 🌐 **CONFIGURACIÓN DE AXIOS**
```javascript
// Configuración base para todas las requests
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,  // IMPORTANTE para cookies de sesión
  headers: {
    'Content-Type': 'application/json'
  }
});
```

---

## 👥 **GESTIÓN DE USUARIOS - ENDPOINTS**

### **1. Listar Todos los Usuarios (con filtros)**
```javascript
// GET /api/user/admin/users/
const getUsers = async (filters = {}) => {
  const params = new URLSearchParams();
  if (filters.role) params.append('role', filters.role);
  if (filters.search) params.append('search', filters.search);
  
  const response = await api.get(`/user/admin/users/?${params}`);
  return response.data;
};

// Ejemplo de uso:
const users = await getUsers({ role: 'diseñador', search: 'juan' });
// Response: { users: [...], total: 5, filters: {...} }
```

### **2. Listar Solo Diseñadores**
```javascript
// GET /api/user/admin/designers/
const getDesigners = async () => {
  const response = await api.get('/user/admin/designers/');
  return response.data;
};

// Response: { designers: [...], total: 3 }
```

### **3. Cambiar Rol de Usuario**
```javascript
// POST /api/user/admin/set-role/
const changeUserRole = async (userId, newRole) => {
  const response = await api.post('/user/admin/set-role/', {
    user_id: userId,
    role: newRole
  });
  return response.data;
};

// Ejemplo:
await changeUserRole(123, 'diseñador');
```

---

## 🎨 **GESTIÓN DE SERVICIOS - ENDPOINTS**

### **1. Listar Servicios Existentes**
```javascript
// GET /api/branding/services/
const getServices = async () => {
  const response = await api.get('/branding/services/');
  return response.data;
};
```

### **2. Crear Nuevo Servicio**
```javascript
// POST /api/branding/services/
const createService = async (serviceData) => {
  const response = await api.post('/branding/services/', {
    name: serviceData.name,
    description: serviceData.description,
    service_type: serviceData.type,
    base_price: serviceData.price,
    features: serviceData.features, // Array de strings
    delivery_time: serviceData.delivery,
    category: serviceData.categoryId // Opcional
  });
  return response.data;
};

// Ejemplo:
await createService({
  name: "Logo Corporativo Premium",
  description: "Logo completo con manual de marca",
  type: "logo",
  price: 500,
  features: ["Logo en múltiples formatos", "Manual de marca", "3 revisiones"],
  delivery: "7-10 días"
});
```

### **3. Listar Categorías de Servicios**
```javascript
// GET /api/branding/service-categories/
const getServiceCategories = async () => {
  const response = await api.get('/branding/service-categories/');
  return response.data;
};
```

---

## 📋 **ASIGNACIÓN DE PROYECTOS - ENDPOINTS**

### **1. Listar Proyectos**
```javascript
// GET /api/branding/projects/
const getProjects = async () => {
  const response = await api.get('/branding/projects/');
  return response.data;
};
```

### **2. Asignar Diseñador a Proyecto**
```javascript
// POST /api/branding/projects/{id}/assign_designer/
const assignDesignerToProject = async (projectId, designerId) => {
  const response = await api.post(`/branding/projects/${projectId}/assign_designer/`, {
    designer_id: designerId
  });
  return response.data;
};

// Ejemplo:
await assignDesignerToProject(123, 456);
// Response: { message: "Diseñador juan_designer asignado al proyecto exitosamente", project: {...} }
```

---

## 🎨 **SERVICIOS PRE-CARGADOS (YA EXISTEN)**

### **Categorías Disponibles:**
- **Identidad Visual** - Logos, colores corporativos
- **Diseño Web** - Sitios web, landing pages  
- **Marketing Digital** - Redes sociales, publicidad
- **Material Gráfico** - Folletos, banners, tarjetas
- **Packaging** - Diseño de envases y etiquetas

### **Servicios de Ejemplo:**
```javascript
const SAMPLE_SERVICES = [
  {
    name: "Logo Básico",
    category: "Identidad Visual",
    price: 150,
    delivery: "3-5 días",
    features: ["Logo en PNG y JPG", "2 revisiones", "Guía de colores básica"]
  },
  {
    name: "Logo Premium", 
    category: "Identidad Visual",
    price: 350,
    delivery: "7-10 días",
    features: ["Logo en múltiples formatos", "Paleta de colores", "Tipografía", "3 revisiones", "Manual de marca básico"]
  },
  {
    name: "Landing Page",
    category: "Diseño Web", 
    price: 400,
    delivery: "5-7 días",
    features: ["Diseño responsive", "Optimización móvil", "2 revisiones", "Archivos para desarrollo"]
  },
  {
    name: "Kit Redes Sociales",
    category: "Marketing Digital",
    price: 200, 
    delivery: "3-5 días",
    features: ["10 posts personalizados", "Stories templates", "Cover para perfiles", "Guía de colores"]
  },
  {
    name: "Tarjetas de Presentación",
    category: "Material Gráfico",
    price: 80,
    delivery: "2-3 días", 
    features: ["Diseño frontal y trasero", "Archivos para impresión", "2 revisiones"]
  }
  // ... y 6 más
];
```

---

## 🖥️ **COMPONENTES SUGERIDOS PARA EL FRONTEND**

### **1. Panel de Usuarios**
```jsx
const AdminUsersPanel = () => {
  const [users, setUsers] = useState([]);
  const [filters, setFilters] = useState({ role: '', search: '' });
  
  // Filtros: dropdown con roles y input de búsqueda
  // Tabla con: ID, Username, Email, Rol, Fecha Registro, Acciones
  // Acciones: botón "Cambiar Rol" que abre modal
};
```

### **2. Selector de Diseñadores**
```jsx
const DesignerSelector = ({ projectId, onAssign }) => {
  const [designers, setDesigners] = useState([]);
  
  // Dropdown con lista de diseñadores
  // Botón "Asignar" que llama a assignDesignerToProject
};
```

### **3. Formulario de Servicios**
```jsx
const ServiceForm = () => {
  // Campos: nombre, descripción, tipo, precio, características, tiempo entrega
  // Selector de categoría
  // Botón "Crear Servicio"
};
```

---

## 🔄 **FLUJO COMPLETO DE TRABAJO**

### **1. Login como Admin**
```javascript
const loginAsAdmin = async () => {
  const response = await api.post('/user/login/', {
    identifier: 'admin',
    password: 'Admin123!'
  });
  // Usuario queda logueado con cookies automáticas
};
```

### **2. Gestionar Usuarios**
```javascript
// 1. Listar usuarios
const users = await getUsers();

// 2. Filtrar por rol
const designers = await getUsers({ role: 'diseñador' });

// 3. Cambiar rol de usuario
await changeUserRole(userId, 'diseñador');
```

### **3. Asignar Proyecto**
```javascript
// 1. Obtener diseñadores disponibles
const { designers } = await getDesigners();

// 2. Asignar diseñador a proyecto
await assignDesignerToProject(projectId, designerId);
// El proyecto automáticamente cambia a "in_progress"
```

### **4. Crear Servicio**
```javascript
await createService({
  name: "Nuevo Servicio",
  description: "Descripción del servicio",
  type: "web",
  price: 300,
  features: ["Característica 1", "Característica 2"],
  delivery: "5-7 días"
});
```

---

## ⚠️ **NOTAS IMPORTANTES**

### **Autenticación:**
- ✅ **Cookies automáticas** - no necesitas manejar tokens manualmente
- ✅ **Sesión persiste** al refrescar la página
- ✅ **withCredentials: true** es OBLIGATORIO en axios

### **Validaciones del Backend:**
- ✅ Solo usuarios con rol `diseñador` pueden ser asignados a proyectos
- ✅ Solo admins pueden acceder a endpoints `/admin/`
- ✅ Validación automática de roles en todas las operaciones

### **Manejo de Errores:**
```javascript
try {
  await changeUserRole(userId, newRole);
} catch (error) {
  if (error.response?.status === 403) {
    // No tienes permisos de admin
  } else if (error.response?.status === 404) {
    // Usuario no encontrado
  }
}
```

---

## 🚀 **TESTING RÁPIDO**

### **1. Verificar Login Admin:**
```javascript
// Login
await api.post('/user/login/', { identifier: 'admin', password: 'Admin123!' });

// Verificar perfil
const profile = await api.get('/user/profile/');
console.log(profile.data.role); // Debe ser 'admin'
```

### **2. Listar Usuarios:**
```javascript
const users = await api.get('/user/admin/users/');
console.log(users.data); // Array de usuarios
```

### **3. Listar Diseñadores:**
```javascript
const designers = await api.get('/user/admin/designers/');
console.log(designers.data); // Solo diseñadores
```

---

## 📞 **ESTADO DEL BACKEND**
- ✅ **31/31 tests pasando**
- ✅ **Todos los endpoints funcionando**
- ✅ **Validaciones implementadas**
- ✅ **Servicios de ejemplo cargados**
- ✅ **CORS configurado para localhost:3000**

**¡El backend está 100% listo! Solo necesitas implementar estos componentes en el frontend.** 🎉
