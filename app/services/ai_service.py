import os
import logging
from google import genai

logger = logging.getLogger(__name__)

async def generate_document_content(prompt: str) -> str:
    """
    Sends the prompt to Gemini and gets the generated document text.
    """
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not found")
        
        # ✅ Correct client initialization
        client = genai.Client(api_key=api_key)
        
        # ✅ Use a valid model
        model_name = "gemini-3-flash-preview"
        
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        
        if response.text:
            return response.text
        else:
            raise ValueError("Empty response from Gemini")
            
    except Exception as e:
        logger.error(f"Error generating content from Gemini: {str(e)}")
        raise e
