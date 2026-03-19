
import os
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

async def generate_document_content(prompt: str) -> str:
    """
    Sends the prompt to Gemini and gets the generated document text.
    """
    try:
        # 1. Obtener la API Key
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not found")
        
        # 2. Configuración obligatoria para google-generativeai
        genai.configure(api_key=api_key)
        
        # 3. Inicialización del modelo (En esta librería NO existe genai.Client)
        # Usamos 'gemini-1.5-flash' que es la versión estable y rápida actual
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        # 4. Generación de contenido
        # Nota: En esta versión se usa generate_content directamente desde el modelo
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        else:
            raise ValueError("Empty response from Gemini")
            
    except Exception as e:
        logger.error(f"Error generating content from Gemini: {str(e)}")
        # Es buena práctica imprimir el error completo en logs para debuggear en Railway
        print(f"DEBUG ERROR: {e}") 
        raise e
