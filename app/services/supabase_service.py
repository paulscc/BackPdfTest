import os
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

# Configuración de variables desde el entorno (.env)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

from typing import Optional

def upload_pdf_to_storage(file_name: str, file_bytes: bytes) -> Optional[str]:
    """
    Sube un archivo PDF al bucket 'Pdf' en Supabase y retorna la URL pública.
    """
    try:
        supabase = get_supabase_client()
        bucket_name = "Pdf"
        
        # Subir el archivo al bucket
        # file_bytes es el contenido binario del PDF
        response = supabase.storage.from_(bucket_name).upload(
            file=file_bytes,
            path=file_name,
            file_options={"content-type": "application/pdf", "upsert": "true"}
        )
        
        # Obtener la URL pública del archivo subido
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
        return public_url
        
    except Exception as e:
        logger.error(f"Error subiendo archivo a Supabase: {str(e)}")
        print(f"DEBUG SUPABASE ERROR: {e}")
        return None

def save_document_record(record_data: dict) -> Optional[dict]:
    """
    Inserta el registro del reporte en la tabla 'generated_documents'.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("generated_documents").insert(record_data).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error guardando registro en Supabase: {str(e)}")
        print(f"DEBUG DB INSERT ERROR: {e}")
        return None

def get_all_documents():
    """
    Obtiene todos los documentos generados, ordenados por fecha descendente.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("generated_documents").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error obteniendo documentos de Supabase: {str(e)}")
        print(f"DEBUG DB SELECT ERROR: {e}")
        return []

def process_and_save_document(file_name: str, file_bytes: bytes, record_data: dict):
    """
    Orquestador en segundo plano: 
    1. Sube el PDF 
    2. Agrega la URL al diccionario de datos 
    3. Guarda en base de datos
    """
    public_url = upload_pdf_to_storage(file_name, file_bytes)
    if public_url:
        record_data["pdf_url"] = public_url
        save_document_record(record_data)
    else:
        logger.error("No se pudo obtener la public_url. No se guardó el registro en BD.")
