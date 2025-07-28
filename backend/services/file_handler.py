from pdf2image import convert_from_bytes
from PIL import Image
import io
from config.settings import Config

def handle_file_upload(file_content: bytes, mime_type: str) -> list[Image.Image]:
    try:
        if mime_type == "application/pdf":
            images = convert_from_bytes(
                file_content,
                poppler_path=Config.POPPLER_PATH,
                fmt='jpeg'  # Force JPEG output
            )
            if not images:
                raise ValueError("PDF conversion failed - empty result")
            return images
        else:
            # Validate image formats
            allowed_image_types = ["image/jpeg", "image/png"]
            test_image = Image.open(io.BytesIO(file_content))
            test_image.verify()  # Check if valid image
            test_image.close()
            return [Image.open(io.BytesIO(file_content))]
    except Exception as e:
        raise ValueError(f"File processing failed: {str(e)}") from e