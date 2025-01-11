from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from io import BytesIO

# Function to generate a PDF and return it as a BytesIO object
def get_pdf(title, sentences, image_objects):
    # Create a BytesIO buffer
    buffer = BytesIO()

    # Create a canvas object using the buffer
    c = canvas.Canvas(buffer, pagesize=letter)

    # Set the title font and position
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(300, 770, title)

    # Define the starting Y position
    y_position = 720
    image_height = 3 * inch  # Fixed height for images
    margin_bottom = 100      # Define bottom margin to avoid content getting cut off

    # Define a style for wrapping text
    styles = getSampleStyleSheet()
    style = styles['Normal']

    # Iterate over the sentences and images
    for i, (sentence, image_object) in enumerate(zip(sentences, image_objects)):
        # Handle sentence with wrapping
        paragraph = Paragraph(sentence, style)
        width, height = paragraph.wrap(450, y_position - margin_bottom)  # Adjust width
        if y_position - height < margin_bottom:
            c.showPage()  # Start a new page if space is insufficient
            y_position = 750  # Reset Y position for the new page

        y_position -= 10  # Small gap before text
        paragraph.drawOn(c, 70, y_position - height)
        y_position -= height + 20

        # Check if there's enough space for the image and move to the next page if necessary
        if y_position - image_height < margin_bottom:
            c.showPage()  # Start a new page if space is insufficient
            y_position = 750  # Reset Y position for the new page

        # Add image if available
        if image_object:
            pil_image = ImageReader(image_object)
            c.drawImage(pil_image, 100, y_position - image_height, width=4 * inch, height=image_height)
        else:
            c.drawString(100, y_position, "[Image Not Available]")  # Fallback if image object is missing

        # Adjust position after image
        y_position -= image_height + 20

        # If the Y position gets too low, start a new page
        if y_position < margin_bottom:
            c.showPage()
            y_position = 750  # Reset Y position for the new page

    # Save the PDF into the BytesIO buffer
    c.save()

    # Move the buffer's position to the beginning
    buffer.seek(0)

    return buffer
