import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def preguntar_con_fecha(prompt):
    # Obtenemos la fecha actual del sistema
    ahora = datetime.now().strftime("%A, %d de %B de %Y")
    
    # Le damos contexto al modelo para que no alucine
    contexto = f"Contexto: Hoy es {ahora}. Responde a la siguiente duda: "
    
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=contexto + prompt
        )
        print(f"\nRespuesta:\n{response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    pregunta = input("¿Qué quieres preguntarle a Gemini? > ")
    preguntar_con_fecha(pregunta)