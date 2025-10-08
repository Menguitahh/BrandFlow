from django.core.management.base import BaseCommand
from django.conf import settings
from user_control.models import Users
from brand_control.models import ServiceCategory, Service


class Command(BaseCommand):
    help = 'Crea un usuario admin por defecto y datos de servicios si no existen'

    def handle(self, *args, **options):
        admin_username = 'admin'
        admin_pass = getattr(settings, 'ADMIN_PASS', None) or 'Admin123!'

        admin, created = Users.objects.get_or_create(username=admin_username, defaults={
            'email': 'admin@example.com',
            'roles': 'admin'
        })
        if created:
            admin.set_password(admin_pass)
            admin.save()
            self.stdout.write(self.style.SUCCESS(f"Admin creado: {admin_username}/{admin_pass}"))
        else:
            self.stdout.write(self.style.WARNING("Admin ya existe"))

        # Crear categorías de branding
        categories_data = [
            {'name': 'Identidad Visual', 'description': 'Logos, colores corporativos y elementos de marca'},
            {'name': 'Diseño Web', 'description': 'Sitios web, landing pages y aplicaciones'},
            {'name': 'Marketing Digital', 'description': 'Redes sociales, publicidad y contenido visual'},
            {'name': 'Material Gráfico', 'description': 'Folletos, banners, tarjetas y papelería'},
            {'name': 'Packaging', 'description': 'Diseño de envases y etiquetas de productos'}
        ]
        
        for cat_data in categories_data:
            ServiceCategory.objects.get_or_create(
                name=cat_data['name'], 
                defaults={'description': cat_data['description']}
            )
        
        # Crear servicios de branding
        services_data = [
            # Identidad Visual
            {
                'name': 'Logo Básico',
                'category': 'Identidad Visual',
                'description': 'Diseño de logo simple con 2 revisiones',
                'service_type': 'logo',
                'base_price': 150,
                'features': ['Logo en PNG y JPG', '2 revisiones', 'Guía de colores básica'],
                'delivery_time': '3-5 días'
            },
            {
                'name': 'Logo Premium',
                'category': 'Identidad Visual',
                'description': 'Logo completo con identidad visual básica',
                'service_type': 'logo',
                'base_price': 350,
                'features': ['Logo en múltiples formatos', 'Paleta de colores', 'Tipografía', '3 revisiones', 'Manual de marca básico'],
                'delivery_time': '7-10 días'
            },
            {
                'name': 'Identidad Corporativa Completa',
                'category': 'Identidad Visual',
                'description': 'Sistema completo de identidad visual',
                'service_type': 'branding',
                'base_price': 800,
                'features': ['Logo principal y variaciones', 'Paleta de colores completa', 'Tipografías', 'Manual de marca detallado', 'Aplicaciones en papelería', '5 revisiones'],
                'delivery_time': '15-20 días'
            },
            
            # Diseño Web
            {
                'name': 'Landing Page',
                'category': 'Diseño Web',
                'description': 'Diseño de página de aterrizaje responsive',
                'service_type': 'web',
                'base_price': 400,
                'features': ['Diseño responsive', 'Optimización móvil', '2 revisiones', 'Archivos para desarrollo'],
                'delivery_time': '5-7 días'
            },
            {
                'name': 'Sitio Web Corporativo',
                'category': 'Diseño Web',
                'description': 'Diseño completo de sitio web empresarial',
                'service_type': 'web',
                'base_price': 1200,
                'features': ['Hasta 5 páginas', 'Diseño responsive', 'Sistema de colores', '3 revisiones', 'Prototipos interactivos'],
                'delivery_time': '10-15 días'
            },
            
            # Marketing Digital
            {
                'name': 'Kit Redes Sociales',
                'category': 'Marketing Digital',
                'description': 'Diseños para redes sociales (Instagram, Facebook, LinkedIn)',
                'service_type': 'social',
                'base_price': 200,
                'features': ['10 posts personalizados', 'Stories templates', 'Cover para perfiles', 'Guía de colores'],
                'delivery_time': '3-5 días'
            },
            {
                'name': 'Campaña Publicitaria',
                'category': 'Marketing Digital',
                'description': 'Diseños para campaña publicitaria completa',
                'service_type': 'advertising',
                'base_price': 500,
                'features': ['Banners web', 'Anuncios redes sociales', 'Material impreso', '3 revisiones'],
                'delivery_time': '7-10 días'
            },
            
            # Material Gráfico
            {
                'name': 'Tarjetas de Presentación',
                'category': 'Material Gráfico',
                'description': 'Diseño de tarjetas de presentación profesionales',
                'service_type': 'print',
                'base_price': 80,
                'features': ['Diseño frontal y trasero', 'Archivos para impresión', '2 revisiones'],
                'delivery_time': '2-3 días'
            },
            {
                'name': 'Folleto Corporativo',
                'category': 'Material Gráfico',
                'description': 'Diseño de folleto promocional',
                'service_type': 'print',
                'base_price': 300,
                'features': ['Diseño 2 caras', 'Hasta 4 páginas', 'Archivos para impresión', '3 revisiones'],
                'delivery_time': '5-7 días'
            },
            
            # Packaging
            {
                'name': 'Diseño de Etiqueta',
                'category': 'Packaging',
                'description': 'Diseño de etiqueta para producto',
                'service_type': 'packaging',
                'base_price': 250,
                'features': ['Diseño frontal y trasero', 'Especificaciones técnicas', 'Archivos para impresión', '2 revisiones'],
                'delivery_time': '4-6 días'
            },
            {
                'name': 'Packaging Completo',
                'category': 'Packaging',
                'description': 'Diseño completo de packaging de producto',
                'service_type': 'packaging',
                'base_price': 600,
                'features': ['Caja principal', 'Etiquetas', 'Manual de usuario', 'Archivos 3D', '4 revisiones'],
                'delivery_time': '10-14 días'
            }
        ]
        
        for service_data in services_data:
            category = ServiceCategory.objects.get(name=service_data['category'])
            Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'category': category,
                    'description': service_data['description'],
                    'service_type': service_data['service_type'],
                    'base_price': service_data['base_price'],
                    'features': service_data['features'],
                    'delivery_time': service_data['delivery_time']
                }
            )
        
        self.stdout.write(self.style.SUCCESS("Servicios de branding creados exitosamente"))


