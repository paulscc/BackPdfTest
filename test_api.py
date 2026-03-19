import requests
import json

url = "http://127.0.0.1:8000/generate-document"

payload = {
    "nombre": "Juan",
    "apellido": "Pérez",
    "direccion": "Av. Siempre Viva 123",
    "telefono": "0999999999",
    "email": "juan@email.com",
    "giro_negocio": "Salud",
    "tamano_empresa": "Mediana empresa",
    "tipo_datos": "Datos de pacientes",
    "tipo_documento": "Política de Protección de Datos Personales"
}

headers = {
    'Content-Type': 'application/json'
}

print("Enviando solicitud...")
response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    print("Documento generado con éxito.")
    with open("test_output.pdf", "wb") as f:
        f.write(response.content)
    print("Guardado exitoso como test_output.pdf")
else:
    print(f"Error {response.status_code}: {response.text}")
