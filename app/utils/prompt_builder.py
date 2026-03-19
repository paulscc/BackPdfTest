from app.models.request_model import DocumentRequest

def build_document_prompt(data: DocumentRequest) -> str:
    return f"""Genera un documento titulado "{data.tipo_documento}" para una empresa del sector {data.giro_negocio}.

Datos del solicitante:
* Nombre: {data.nombre} {data.apellido}
* Dirección: {data.direccion}
* Teléfono: {data.telefono}
* Email: {data.email}

Características de la organización:
* Tamaño de empresa: {data.tamano_empresa}
* Tipo de datos tratados: {data.tipo_datos}

El documento debe:
* Estar en español
* Tener estructura formal: título, introducción, desarrollo por secciones y conclusión
* Ser claro, profesional y bien redactado
* Estar adaptado al sector indicado
* Incluir secciones como: objetivo, alcance, responsabilidades y medidas de seguridad
"""
