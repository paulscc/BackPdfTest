from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import re
import html  # <--- Agregamos esto para limpiar el texto

def create_pdf_from_text(title: str, text: str) -> BytesIO:
    """
    Generates a PDF file in memory from the given title and text.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    
    title_style = styles['Heading1']
    title_style.alignment = 1 
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        spaceAfter=12,
        leading=14
    )
    
    story = []
    
    # Title (escapamos el título también por seguridad)
    story.append(Paragraph(html.escape(title), title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # --- PASO CRUCIAL: Limpieza de caracteres XML/HTML ---
        # Primero escapamos todo (&, <, >) para que ReportLab no se rompa
        line = html.escape(line)
        
        # Ahora que está seguro, reemplazamos las etiquetas de Markdown por 
        # etiquetas que ReportLab SÍ entiende (usamos un replace simple o regex)
        line = re.sub(r'(\*\*)(.*?)\1', r'<b>\2</b>', line)
        line = re.sub(r'(\*)(.*?)\1', r'<i>\2</i>', line)

        # Manejo de Headers
        if line.startswith('### '):
            clean_line = line.replace('### ', '')
            story.append(Paragraph(clean_line, styles['Heading3']))
            story.append(Spacer(1, 0.1 * inch))
        elif line.startswith('## '):
            clean_line = line.replace('## ', '')
            story.append(Paragraph(clean_line, styles['Heading2']))
            story.append(Spacer(1, 0.1 * inch))
        elif line.startswith('# '):
            clean_line = line.replace('# ', '')
            story.append(Paragraph(clean_line, styles['Heading1']))
            story.append(Spacer(1, 0.1 * inch))
            
        # Manejo de Listas
        elif line.startswith('* ') or line.startswith('- '):
            bullet_style = ParagraphStyle(
                'Bullet',
                parent=styles['Normal'],
                leftIndent=20,
                firstLineIndent=-10,
                spaceAfter=6
            )
            # Quitamos el marcador de markdown y ponemos el punto real
            item_text = line[2:] 
            story.append(Paragraph(f"• {item_text}", bullet_style))
            
        else:
            # Párrafo normal
            story.append(Paragraph(line, body_style))
            
    doc.build(story)
    buffer.seek(0)
    return buffer
