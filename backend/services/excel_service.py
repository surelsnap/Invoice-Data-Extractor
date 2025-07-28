from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import io

def create_excel(data: list[dict]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoice Data"
    
    # Header styling
    header_font = Font(bold=True)
    header_alignment = Alignment(horizontal="center")
    
    # Write metadata
    ws.append(["Field", "Value"])
    for row in ws.iter_rows(min_row=1, max_row=1):
        for cell in row:
            cell.font = header_font
            cell.alignment = header_alignment
    
    # Add data from all pages
    for page_num, page_data in enumerate(data, 1):
        ws.append([f"Page {page_num} Data"])
        ws.append(["Vendor Name", page_data.get("vendor_name")])
        ws.append(["Invoice Number", page_data.get("invoice_number")])
        ws.append(["Date", page_data.get("date")])
        ws.append(["Total Amount", page_data.get("total_amount")])
        ws.append(["Items"])
        
        for item in page_data.get("items", []):
            ws.append(["", item])
        
        ws.append([])  # Add empty row between pages
    
    # Set column widths
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 40
    
    # Save to bytes buffer
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.read()