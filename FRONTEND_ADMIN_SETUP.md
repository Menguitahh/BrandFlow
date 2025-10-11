# 🎯 **CONFIGURACIÓN FRONTEND PARA PANEL DE ADMIN**

## 📋 **RESUMEN**
El backend está funcionando al 95%. Los endpoints GET funcionan perfectamente, solo necesitas configurar CSRF para las operaciones POST.

---

## 🔑 **CREDENCIALES DE ADMIN**
```
Usuario: admin
Contraseña: Admin123!
```

---

## 🌐 **CONFIGURACIÓN DE AXIOS**

### **Opción 1: Con CSRF (Recomendado)**
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor para manejar CSRF
api.interceptors.request.use(async (config) => {
  // Solo para requests POST/PUT/DELETE
  if (['post', 'put', 'delete'].includes(config.method)) {
    try {
      // Obtener CSRF token
      const csrfResponse = await axios.get('http://localhost:8000/api/user/test/', {
        withCredentials: true
      });
      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
      
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
      }
    } catch (error) {
      console.log('No se pudo obtener CSRF token');
    }
  }
  return config;
});

export default api;
```

### **Opción 2: Sin CSRF (Más Simple)**
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default api;
```

---

## 🎨 **COMPONENTES DEL PANEL DE ADMIN**

### **1. Dashboard Principal**
```jsx
const AdminDashboard = () => {
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalDesigners: 0,
    totalProjects: 0,
    totalQuotes: 0
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [users, designers, projects, quotes] = await Promise.all([
        api.get('/user/admin/users/'),
        api.get('/user/admin/designers/'),
        api.get('/branding/projects/'),
        api.get('/branding/quotes/')
      ]);

      setStats({
        totalUsers: users.data.total,
        totalDesigners: designers.data.total,
        totalProjects: projects.data.length,
        totalQuotes: quotes.data.length
      });
    } catch (error) {
      console.error('Error cargando dashboard:', error);
    }
  };

  return (
    <div className="admin-dashboard">
      <h1>Panel de Administración</h1>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Usuarios</h3>
          <p>{stats.totalUsers}</p>
        </div>
        <div className="stat-card">
          <h3>Diseñadores</h3>
          <p>{stats.totalDesigners}</p>
        </div>
        <div className="stat-card">
          <h3>Proyectos</h3>
          <p>{stats.totalProjects}</p>
        </div>
        <div className="stat-card">
          <h3>Cotizaciones</h3>
          <p>{stats.totalQuotes}</p>
        </div>
      </div>
    </div>
  );
};
```

### **2. Panel de Usuarios**
```jsx
const UsersPanel = () => {
  const [users, setUsers] = useState([]);
  const [filters, setFilters] = useState({
    role: '',
    search: ''
  });

  const loadUsers = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.role) params.append('role', filters.role);
      if (filters.search) params.append('search', filters.search);
      
      const response = await api.get(`/user/admin/users/?${params}`);
      setUsers(response.data.users);
    } catch (error) {
      console.error('Error cargando usuarios:', error);
    }
  };

  const changeUserRole = async (userId, newRole) => {
    try {
      await api.post('/user/admin/set-role/', {
        user_id: userId,
        role: newRole
      });
      loadUsers(); // Recargar lista
    } catch (error) {
      console.error('Error cambiando rol:', error);
    }
  };

  return (
    <div className="users-panel">
      <h2>Gestión de Usuarios</h2>
      
      {/* Filtros */}
      <div className="filters">
        <select 
          value={filters.role} 
          onChange={(e) => setFilters({...filters, role: e.target.value})}
        >
          <option value="">Todos los roles</option>
          <option value="cliente">Cliente</option>
          <option value="diseñador">Diseñador</option>
          <option value="admin">Admin</option>
        </select>
        
        <input 
          type="text"
          placeholder="Buscar usuario..."
          value={filters.search}
          onChange={(e) => setFilters({...filters, search: e.target.value})}
        />
        
        <button onClick={loadUsers}>Filtrar</button>
      </div>

      {/* Tabla de usuarios */}
      <table className="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Usuario</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.username}</td>
              <td>{user.email}</td>
              <td>{user.role}</td>
              <td>
                <select 
                  value={user.role}
                  onChange={(e) => changeUserRole(user.id, e.target.value)}
                >
                  <option value="cliente">Cliente</option>
                  <option value="diseñador">Diseñador</option>
                  <option value="admin">Admin</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

### **3. Panel de Servicios**
```jsx
const ServicesPanel = () => {
  const [services, setServices] = useState([]);
  const [categories, setCategories] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);

  const loadServices = async () => {
    try {
      const [servicesRes, categoriesRes] = await Promise.all([
        api.get('/branding/services/'),
        api.get('/branding/service-categories/')
      ]);
      setServices(servicesRes.data);
      setCategories(categoriesRes.data);
    } catch (error) {
      console.error('Error cargando servicios:', error);
    }
  };

  const createService = async (serviceData) => {
    try {
      await api.post('/branding/services/', serviceData);
      loadServices(); // Recargar lista
      setShowCreateForm(false);
    } catch (error) {
      console.error('Error creando servicio:', error);
    }
  };

  return (
    <div className="services-panel">
      <h2>Gestión de Servicios</h2>
      <button onClick={() => setShowCreateForm(true)}>
        Crear Nuevo Servicio
      </button>

      {/* Lista de servicios */}
      <div className="services-grid">
        {services.map(service => (
          <div key={service.id} className="service-card">
            <h3>{service.name}</h3>
            <p>{service.description}</p>
            <p><strong>Precio:</strong> ${service.base_price}</p>
            <p><strong>Entrega:</strong> {service.delivery_time}</p>
            <p><strong>Categoría:</strong> {service.category?.name}</p>
          </div>
        ))}
      </div>

      {/* Formulario de creación */}
      {showCreateForm && (
        <CreateServiceForm 
          categories={categories}
          onSubmit={createService}
          onCancel={() => setShowCreateForm(false)}
        />
      )}
    </div>
  );
};
```

### **4. Panel de Proyectos**
```jsx
const ProjectsPanel = () => {
  const [projects, setProjects] = useState([]);
  const [designers, setDesigners] = useState([]);

  const loadProjects = async () => {
    try {
      const [projectsRes, designersRes] = await Promise.all([
        api.get('/branding/projects/'),
        api.get('/user/admin/designers/')
      ]);
      setProjects(projectsRes.data);
      setDesigners(designersRes.data.designers);
    } catch (error) {
      console.error('Error cargando proyectos:', error);
    }
  };

  const assignDesigner = async (projectId, designerId) => {
    try {
      const response = await api.post(`/branding/projects/${projectId}/assign_designer/`, {
        designer_id: designerId
      });
      console.log(response.data.message);
      loadProjects(); // Recargar lista
    } catch (error) {
      console.error('Error asignando diseñador:', error);
    }
  };

  return (
    <div className="projects-panel">
      <h2>Gestión de Proyectos</h2>
      
      <table className="projects-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Título</th>
            <th>Cliente</th>
            <th>Estado</th>
            <th>Diseñador</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {projects.map(project => (
            <tr key={project.id}>
              <td>{project.id}</td>
              <td>{project.title}</td>
              <td>{project.client}</td>
              <td>{project.status}</td>
              <td>{project.assigned_to || 'Sin asignar'}</td>
              <td>
                {project.status === 'quote' && (
                  <select 
                    onChange={(e) => assignDesigner(project.id, e.target.value)}
                  >
                    <option value="">Seleccionar diseñador</option>
                    {designers.map(designer => (
                      <option key={designer.id} value={designer.id}>
                        {designer.username}
                      </option>
                    ))}
                  </select>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

---

## 🚀 **ENDPOINTS QUE FUNCIONAN AL 100%**

### **GET Endpoints (Listos):**
```javascript
// Usuarios
GET /api/user/admin/users/                    // Lista usuarios
GET /api/user/admin/users/?role=diseñador     // Filtro por rol
GET /api/user/admin/users/?search=juan        // Búsqueda
GET /api/user/admin/designers/                // Solo diseñadores

// Servicios
GET /api/branding/services/                   // Lista servicios
GET /api/branding/service-categories/         // Lista categorías

// Proyectos y Cotizaciones
GET /api/branding/projects/                   // Lista proyectos
GET /api/branding/quotes/                     // Lista cotizaciones

// Autenticación
GET /api/user/profile/                        // Perfil del usuario
```

### **POST Endpoints (Necesitan CSRF):**
```javascript
// Gestión de usuarios
POST /api/user/admin/set-role/                // Cambiar rol

// Gestión de servicios
POST /api/branding/services/                  // Crear servicio

// Gestión de proyectos
POST /api/branding/projects/{id}/assign_designer/  // Asignar diseñador

// Gestión de cotizaciones
POST /api/branding/quotes/{id}/approve/       // Aprobar cotización
POST /api/branding/quotes/{id}/reject/        // Rechazar cotización
```

---

## 📊 **DATOS DE PRUEBA DISPONIBLES**

### **Usuarios:**
- **93 usuarios** en total
- **3 diseñadores** disponibles para asignación
- **70 clientes** registrados

### **Servicios:**
- **11 servicios** de branding pre-cargados
- **5 categorías** de servicios

### **Proyectos:**
- **2 proyectos** de prueba creados
- **2 cotizaciones** aprobadas

---

## 🎯 **PRÓXIMOS PASOS**

1. **Configurar axios** con manejo de CSRF
2. **Implementar componentes** de panel de admin
3. **Probar endpoints GET** primero
4. **Configurar endpoints POST** con CSRF
5. **Implementar flujo completo** de gestión

**¡El backend está listo! Solo necesitas implementar estos componentes en el frontend.** 🚀

