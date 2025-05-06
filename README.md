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


## 🔗 Relaciones entre Modelos

### 🧑 Usuario
- Tiene un **Carrito** (relación uno a uno).
- Puede realizar múltiples **Pedidos**.
- Puede escribir múltiples **Reseñas**.

### 🛒 Carrito
- Pertenece a un **Usuario**.
- Contiene múltiples **Detalle_Carrito**, cada uno asociado a un **Producto**.

### 📦 Detalle_Carrito
- Pertenece a un **Carrito**.
- Está asociado a un único **Producto**.
- Indica la **cantidad** de un producto en el carrito.

### 🎨 Producto
- Pertenece a una **Categoría**.
- Puede estar en múltiples **Detalle_Carrito** y **Detalle_Pedido**.
- Puede tener múltiples **Reseñas**.

### 🗂️ Categoría
- Contiene múltiples **Productos**.

### 🧾 Pedido
- Pertenece a un **Usuario**.
- Contiene múltiples **Detalle_Pedido**.
- Tiene un único **Pago** asociado.

### 🧮 Detalle_Pedido
- Pertenece a un **Pedido**.
- Está asociado a un único **Producto**.
- Indica la **cantidad** y el **precio unitario** del producto al momento del pedido.

### 💳 Pago
- Pertenece a un único **Pedido**.
- Incluye detalles como el **método**, **estado** y **monto** del pago.

### 📝 Reseña
- Está asociada a un **Usuario** y a un **Producto**.
