import io
import logging
from utils.logger import logger
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from config.settings import Config
from services.gemini_services import process_invoice
from services.excel_service import create_excel
from services.file_handler import handle_file_upload
from utils.data_validation import validate_gemini_response
from utils.logger import configure_logging

import os
print("GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))

# Initialize application
app = FastAPI(title="Invoice Data Extractor")
configure_logging()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload", summary="Process invoice file")
async def upload_file(file: UploadFile = File(...)):
    """
    Process an invoice file and return extracted data in Excel format
    """
    try:
        logger.debug(f"Started processing {file.filename}")
        # Validate file input
        if file.content_type not in Config.ALLOWED_MIME_TYPES:
            raise HTTPException(400, "Unsupported file type")
        
        if file.size > Config.MAX_FILE_SIZE:
            raise HTTPException(413, f"File size exceeds {Config.MAX_FILE_SIZE_MB}MB limit")

        # Process file
        file_content = await file.read()
        processed_images = handle_file_upload(file_content, file.content_type)
        
        # Extract data using Gemini
        extracted_data = []
        for idx, image in enumerate(processed_images):
            # Set correct MIME type for images from PDF
            image_mime_type = "image/jpeg" if file.content_type == "application/pdf" else file.content_type
            response_text = process_invoice(image, image_mime_type)
            validated_data = validate_gemini_response(response_text)
            extracted_data.append(validated_data)
            logging.info(f"Processed page {idx + 1} successfully")

        # Generate Excel file
        excel_file = create_excel(extracted_data)

        logger.debug("Processing completed successfully")
        return StreamingResponse(
            io.BytesIO(excel_file),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=invoice_data.xlsx",
                "X-Accel-Buffering": "no"
            }
        )

    except Exception as e:
        logger.error(f"Full error details: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Processing failed: {type(e).__name__} - {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)