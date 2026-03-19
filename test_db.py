import asyncio
from dotenv import load_dotenv
load_dotenv()

from app.services.supabase_service import process_and_save_document, get_all_documents, get_supabase_client

def test_supabase():
    print("Iniciando prueba de conexión directa a Supabase...")
    try:
        sb = get_supabase_client()
        # Prueba 1: Leer tabla
        print("1. Intentando leer la tabla generated_documents...")
        res = sb.table("generated_documents").select("*").limit(1).execute()
        print("Lectura correcta:", res.data)
        
        # Prueba 2: Insertar un dummy record
        print("2. Intentando insertar un registro mock...")
        mock_data = {
            "nombre": "Test",
            "apellido": "User",
            "email": "test@example.com",
            "telefono": "123",
            "direccion": "123 Test St",
            "giro_negocio": "IT",
            "tamano_empresa": "1",
            "tipo_datos": "Test",
            "tipo_documento": "Mock PDF",
            "content": "Contenido de test",
            "pdf_url": "https://example.com/mock.pdf"
        }
        res_insert = sb.table("generated_documents").insert(mock_data).execute()
        print("Inserción correcta:", res_insert.data)
        
        # Prueba 3: Storage (opcional si es lo que falla)
        print("3. Probando flujo completo (Storage + BD)...")
        process_and_save_document("test_mock.pdf", b"mock content", mock_data)
        print("Flujo completo ejecutado.")
        
    except Exception as e:
        import traceback
        print("🔥 FALLO DETECTADO 🔥")
        traceback.print_exc()

if __name__ == "__main__":
    test_supabase()
