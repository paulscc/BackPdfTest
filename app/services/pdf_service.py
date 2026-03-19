from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import re

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
    title_style.alignment = 1 # Center alignment
    
    # Custom body style for spacing
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        spaceAfter=12,
        leading=14
    )
    
    story = []
    
    # Title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Clean text and split into paragraphs
    # Gemini outputs markdown so handle some basic translation to reportlab
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Parse basic markdown headers
        if line.startswith('### '):
            story.append(Paragraph(line.replace('### ', ''), styles['Heading3']))
            story.append(Spacer(1, 0.1 * inch))
        elif line.startswith('## '):
            story.append(Paragraph(line.replace('## ', ''), styles['Heading2']))
            story.append(Spacer(1, 0.1 * inch))
        elif line.startswith('# '):
            story.append(Paragraph(line.replace('# ', ''), styles['Heading1']))
            story.append(Spacer(1, 0.1 * inch))
        elif line.startswith('* ') or line.startswith('- '):
            # Transform markdown bold to html bold supported by reportlab
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            # Add bullet point indentation
            bullet_style = ParagraphStyle(
                'Bullet',
                parent=styles['Normal'],
                leftIndent=20,
                firstLineIndent=-10,
                spaceAfter=6
            )
            # Use standard bullet character
            item_text = line[2:] 
            story.append(Paragraph(f"• {item_text}", bullet_style))
        else:
            # Transform markdown bold to html bold
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            story.append(Paragraph(line, body_style))
            
    # Build it
    doc.build(story)
    
    # Reset buffer position to start so it can be read
    buffer.seek(0)
    return buffer
