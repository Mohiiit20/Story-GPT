from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

# Register a font that supports Marathi (Unicode)
font_path = "frontend/assets/NotoSansDevanagari-Regular.ttf"  # Update with your font's path
pdfmetrics.registerFont(TTFont("NotoSansDevanagari", font_path))

# Function to generate a PDF and return it as a BytesIO object
def get_pdf(title, sentences, image_objects):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Set the title font to Unicode-supported font
    c.setFont("NotoSansDevanagari", 20)
    c.drawCentredString(300, 770, title)

    y_position = 720
    image_height = 3 * inch
    margin_bottom = 100

    # Define a style that uses the registered font
    styles = getSampleStyleSheet()
    unicode_style = ParagraphStyle(
        "UnicodeStyle",
        parent=styles["Normal"],
        fontName="NotoSansDevanagari",
        fontSize=12,
        leading=15,  # Line spacing
    )

    for i, (sentence, image_object) in enumerate(zip(sentences, image_objects)):
        paragraph = Paragraph(sentence, unicode_style)
        width, height = paragraph.wrap(450, y_position - margin_bottom)

        if y_position - height < margin_bottom:
            c.showPage()
            c.setFont("NotoSansDevanagari", 20)  # Reset font on new page
            y_position = 750

        y_position -= 10
        paragraph.drawOn(c, 70, y_position - height)
        y_position -= height + 20

        if y_position - image_height < margin_bottom:
            c.showPage()
            c.setFont("NotoSansDevanagari", 20)  # Reset font on new page
            y_position = 750

        if image_object:
            pil_image = ImageReader(image_object)
            c.drawImage(pil_image, 100, y_position - image_height, width=4 * inch, height=image_height)
        else:
            c.drawString(100, y_position, "[Image Not Available]")

        y_position -= image_height + 20

        if y_position < margin_bottom:
            c.showPage()
            c.setFont("NotoSansDevanagari", 20)  # Reset font on new page
            y_position = 750

    c.save()
    buffer.seek(0)
    return buffer
