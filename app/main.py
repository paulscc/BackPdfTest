from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- 1. Importar el middleware
from dotenv import load_dotenv
from app.routes import document

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="Generador de Documentos Legales",
    description="API que utiliza Gemini para generar documentos dinámicos en PDF",
    version="1.0.0"
)

# 2. Configurar los orígenes permitidos (CORS)
# Añadimos tanto tu URL de Render como la de local para que no dejes de poder probar en tu PC
origins = [
    "https://frontpdftests.onrender.com",
    "http://localhost:5173",  # Puerto por defecto de Vite
    "http://localhost:3000",  # Puerto por defecto de React común
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Permitir estos dominios
    allow_credentials=True,
    allow_methods=["*"],              # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],              # Permitir todos los encabezados (Content-Type, etc.)
)

# Incluir las rutas del documento
app.include_router(document.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Generador de Documentos. Ve a /docs para ver la documentación de la API."}

if __name__ == "__main__":
    import uvicorn
    # En Render, el puerto se asigna dinámicamente, pero uvicorn.run aquí es para local
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
