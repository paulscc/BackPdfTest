from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.request_model import DocumentRequest
from app.utils.prompt_builder import build_document_prompt
from app.services.ai_service import generate_document_content
from app.services.pdf_service import create_pdf_from_text
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/generate-document")
async def generate_document(request: DocumentRequest):
    try:
        # 1. Valida y construye el prompt con los datos del request
        prompt = build_document_prompt(request)
        
        # 2. Obtiene el contenido redactado enviando el prompt a la API de Gemini
        text_content = await generate_document_content(prompt)
        
        # 3. Convierte el texto obtenido en un archivo PDF en memoria
        pdf_buffer = create_pdf_from_text(request.tipo_documento, text_content)
        
        # 4. Retorna el StreamingResponse con los headers correctos para la descarga
        filename = f"documento_{request.nombre}_{request.apellido}".lower().replace(" ", "_")
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}.pdf"'
        }
        
        return StreamingResponse(
            pdf_buffer, 
            media_type="application/pdf", 
            headers=headers
        )
        
    except ValueError as ve:
        logger.error(f"Validation Error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Ocurrió un error inesperado al procesar la solicitud de documento.")
