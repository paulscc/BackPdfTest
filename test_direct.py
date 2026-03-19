import asyncio
from dotenv import load_dotenv
load_dotenv()

from app.models.request_model import DocumentRequest
from app.utils.prompt_builder import build_document_prompt
from app.services.ai_service import generate_document_content
from app.services.pdf_service import create_pdf_from_text

async def main():
    try:
        request = DocumentRequest(
            nombre="Juan",
            apellido="Perez",
            direccion="test",
            telefono="123",
            email="juan@email.com",
            giro_negocio="Salud",
            tamano_empresa="Mediana",
            tipo_datos="Pacientes",
            tipo_documento="Politica"
        )
        prompt = build_document_prompt(request)
        print("Obteniendo contenido AI...")
        content = await generate_document_content(prompt)
        print("Creando PDF...")
        pdf = create_pdf_from_text(request.tipo_documento, content)
        print("Exito! PDF length:", len(pdf.getvalue()))
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
