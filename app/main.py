from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import document

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI(
    title="Generador de Documentos Legales",
    description="API que utiliza Gemini para generar documentos dinámicos en PDF",
    version="1.0.0"
)

# Incluir las rutas del documento
app.include_router(document.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Generador de Documentos. Ve a /docs para ver la documentación de la API."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
