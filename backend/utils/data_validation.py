import json
import logging
from datetime import datetime

REQUIRED_FIELDS = [
    "vendor_name",
    "invoice_number",
    "date",
    "total_amount"
]

def validate_gemini_response(response_text: str) -> dict:
    try:
        json_str = response_text.split("```")[1] if "```" in response_text else response_text
        json_str = json_str.replace("json\n", "").strip()
        
        # Handle single quotes
        json_str = json_str.replace("'", '"')
        # Parse JSON
        data = json.loads(json_str)
        
        # Validate required fields
        for field in REQUIRED_FIELDS:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
            
        # Validate date format
        try:
            datetime.strptime(data["date"], "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format, expected YYYY-MM-DD")
            
        # Validate total amount
        if not isinstance(data["total_amount"], (int, float)):
            raise ValueError("Total amount must be numeric")
            
        # Validate items
        if not isinstance(data.get("items", []), list):
            raise ValueError("Items must be an array")
            
        return data
        
    except (IndexError, json.JSONDecodeError) as e:
        logging.error(f"Invalid JSON structure: {response_text}")
        raise ValueError("Invalid response format from Gemini API") from e