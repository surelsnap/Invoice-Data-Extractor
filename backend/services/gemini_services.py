import google.generativeai as genai
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel
from google.api_core import exceptions
from config.settings import Config
from PIL import Image
import io
import time

configure(api_key=Config.GEMINI_API_KEY)
model = GenerativeModel('gemini-1.5-pro-latest')

PROMPT_TEMPLATE = """Analyze this invoice document and extract structured data:
- vendor_name (string)
- invoice_number (string)
- date (string in YYYY-MM-DD format)
- total_amount (numeric)
- items (array of product/service descriptions)

Return ONLY valid JSON. Example:
{
  "vendor_name": "ABC Corp",
  "invoice_number": "INV-2023-001",
  "date": "2023-07-15",
  "total_amount": 2499.99,
  "items": ["Product A", "Service B"]
}"""

def process_invoice(image: Image.Image, mime_type: str, max_retries: int = 2) -> str:
    """
    Process invoice image with retry mechanism for quota limits
    """
    for attempt in range(max_retries + 1):
        try:
            # Convert PIL Image to bytes with explicit format
            img_byte_arr = io.BytesIO()
            
            # Determine image format from mime_type
            img_format = "JPEG" if "jpeg" in mime_type.lower() else "PNG"
            image.save(img_byte_arr, format=img_format)
            img_bytes = img_byte_arr.getvalue()

            response = model.generate_content(
                contents=[
                    {"role": "user", "parts": [PROMPT_TEMPLATE]},
                    {"role": "user", "parts": [{"mime_type": mime_type, "data": img_bytes}]}
                ]
            )
            return response.text
            
        except exceptions.ResourceExhausted as e:
            if "429" in str(e) and attempt < max_retries:
                # Wait before retrying (exponential backoff)
                wait_time = (2 ** attempt) * 5  # 5s, 10s, 20s
                time.sleep(wait_time)
                continue
            else:
                raise RuntimeError("API quota exceeded. Please wait a moment and try again, or check your Gemini API billing plan.") from e
        except exceptions.InvalidArgument as e:
            raise RuntimeError(f"Invalid request to Gemini API: {str(e)}") from e
        except exceptions.PermissionDenied as e:
            raise RuntimeError("Invalid or missing API key. Please check your Gemini API configuration.") from e
        except Exception as e:
            raise RuntimeError(f"Gemini processing failed: {str(e)}") from e
    
    # If we get here, all retries failed
    raise RuntimeError("API quota exceeded after all retry attempts. Please check your Gemini API billing plan.")