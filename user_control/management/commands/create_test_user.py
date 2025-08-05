from django.core.management.base import BaseCommand
from user_control.models import Users

class Command(BaseCommand):
    help = 'Crea un usuario de prueba para testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='testuser',
            help='Username del usuario de prueba'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='test@example.com',
            help='Email del usuario de prueba'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='Test123!',
            help='Password del usuario de prueba'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        try:
            # Verificar si el usuario ya existe
            if Users.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Usuario {username} ya existe')
                )
                return

            # Crear usuario de prueba
            user = Users.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name='Test',
                last_name='User',
                phone='123456789',
                address='Calle Test 123',
                roles='cliente'
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Usuario de prueba creado exitosamente:\n'
                    f'Username: {username}\n'
                    f'Email: {email}\n'
                    f'Password: {password}'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creando usuario: {str(e)}')
            ) 