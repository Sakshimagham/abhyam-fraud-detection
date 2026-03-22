import pytesseract
from PIL import Image
import io

def extract_text_from_image(uploaded_file):
    """
    Extract text from an uploaded image file using Tesseract OCR.
    Supports multiple Indian languages.
    """
    try:
        image = Image.open(io.BytesIO(uploaded_file.read()))
        # Use language packs: English + Indian languages
        text = pytesseract.image_to_string(image, lang='eng+hin+mar+tam+tel+kan+mal+guj+ben+pan')
        return text.strip()
    except Exception as e:
        return f"OCR error: {str(e)}"