import requests

# Crea una sesión para mantener las cookies entre requests
session = requests.Session()

# Primero, login
login_url = 'http://127.0.0.1:8000/api/user/login/'
login_data = {
    'identifier': 'juanperez92',  # Cambia por tu username o email
    'password': 'ClaveFuerte456!',   # Cambia por tu contraseña
}
login_response = session.post(login_url, json=login_data)
print('Login status:', login_response.status_code)
print('Login response:', login_response.text)


csrf_token = session.cookies.get('csrftoken')
print('csrf_token:', csrf_token)

# Ahora, logout usando la misma sesión (misma cookie)
logout_url = 'http://127.0.0.1:8000/api/user/logout/'
headers = {'X-CSRFToken': csrf_token}
logout_response = session.post(logout_url, headers=headers)
print('Logout status:', logout_response.status_code)
print('Logout response:', logout_response.text) 