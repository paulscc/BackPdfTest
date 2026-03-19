from pydantic import BaseModel, EmailStr
from typing import Optional

class DocumentRequest(BaseModel):
    nombre: str
    apellido: str
    direccion: str
    telefono: str
    email: str
    giro_negocio: str
    tamano_empresa: str
    tipo_datos: str
    tipo_documento: str
