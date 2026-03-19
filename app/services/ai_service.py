import os
import logging
from google import genai

logger = logging.getLogger(__name__)

async def generate_document_content(prompt: str) -> str:
    """
    Sends the prompt to Gemini and gets the generated document text.
    """
    try:
        # 1. Obtener la API Key dinámica para evitar problemas de orden de importación
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not found")
        
        # 2. Inicializar el cliente oficial y más reciente genai.Client
        client = genai.Client(api_key=api_key)
        
        # 3. Este modelo es el que se confirmó que funciona con tu API Key en maiin.py
        model_name = "gemini-3-flash-preview"
        
        # 4. Generación de contenido
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        
        if response and response.text:
            return response.text
        else:
            raise ValueError("Empty response from Gemini")
            
    except Exception as e:
        logger.error(f"Error generating content from Gemini: {str(e)}")
        print(f"DEBUG ERROR: {e}") 
        raise e
