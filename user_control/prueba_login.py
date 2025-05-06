import requests

url = 'http://127.0.0.1:8000/api/user/login/'

data = {
    'username': 'Menga_Admin',
    'password': 'Peritomoreno434',
    'roles': 'cliente',
}

response = requests.post(url, json=data)

print("Código de estado:", response.status_code)
try:
    json_response = response.json()
    print("Respuesta JSON:", json_response)
except ValueError:
    print("⚠️ La respuesta no es JSON. Contenido crudo:")
    print(response.text)
