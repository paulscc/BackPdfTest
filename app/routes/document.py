from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from app.models.request_model import DocumentRequest
from app.utils.prompt_builder import build_document_prompt
from app.services.ai_service import generate_document_content
from app.services.pdf_service import create_pdf_from_text
from app.services.supabase_service import process_and_save_document, get_all_documents
import logging
import time

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/generate-document")
async def generate_document(request: DocumentRequest, background_tasks: BackgroundTasks):
    try:
        # 1. Valida y construye el prompt con los datos del request
        prompt = build_document_prompt(request)
        
        # 2. Obtiene el contenido redactado enviando el prompt a la API de Gemini
        text_content = await generate_document_content(prompt)
        
        # 3. Convierte el texto obtenido en un archivo PDF en memoria
        pdf_buffer = create_pdf_from_text(request.tipo_documento, text_content)
        
        # Guardar los bytes crudos y crear el nombre de archivo con timestamp
        pdf_bytes = pdf_buffer.getvalue()
        filename = f"documento_{request.nombre}_{request.apellido}_{int(time.time())}.pdf".lower().replace(" ", "_")
        
        # Preparar los datos para la base de datos coincidiendo con la tabla generated_documents
        record_data = {
            "nombre": request.nombre,
            "apellido": request.apellido,
            "email": request.email,
            "telefono": request.telefono,
            "direccion": request.direccion,
            "giro_negocio": request.giro_negocio,
            "tamano_empresa": request.tamano_empresa,
            "tipo_datos": request.tipo_datos,
            "tipo_documento": request.tipo_documento,
            "content": text_content
        }
        
        # 4. Enviar Tarea en segundo plano a Supabase (Storage + BD)
        background_tasks.add_task(process_and_save_document, filename, pdf_bytes, record_data)
        
        # 5. Retorna el StreamingResponse con los headers correctos para la descarga
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'
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

@router.get("/documents")
async def fetch_documents():
    """
    Endpoint para recuperar todos los documentos generados.
    Ideal para presentar en una tabla de DataGrid en el Frontend.
    """
    try:
        documents = get_all_documents()
        return documents
    except Exception as e:
        logger.error(f"Error fetching documents: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener los documentos.")
