from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime
from pathlib import Path
from typing import Any
from app.models import FinancePayload


def draw_page_header(canvas_obj: Canvas, doc: Any, payload: FinancePayload, page_num: int) -> None:
    """Draw header on each page with logo, title, farmer name, and timestamp"""
    canvas_obj.saveState()
    
    # Logo (top-left) - use absolute path
    logo_path = Path("static/gramiq_logo.jpg").resolve()
    print(f"🔍 Looking for logo at: {logo_path}")
    print(f"✅ Logo exists: {logo_path.exists()}")
    
    if logo_path.exists():
        try:
            canvas_obj.drawImage(str(logo_path), 0.5*inch, 9.8*inch, width=2*inch, height=2*inch)
            print(f"✅ Logo drawn successfully")
        except Exception as e:
            print(f"❌ Error drawing logo: {e}")
    else:
        print(f"⚠️ Logo file not found at {logo_path}")
    
    # Dynamic report title: crop_acres_season_year (center)
    title = f"{payload.farmer_details.crop_name.upper()} {payload.farmer_details.total_acres} acres | {payload.farmer_details.season}_{datetime.now().year}"
    canvas_obj.setFont("Helvetica-Bold", 18)
    canvas_obj.drawCentredString(4.25*inch, 10.8*inch, title)
    
    # Farmer Name (top-right)
    canvas_obj.setFont("Helvetica", 12)
    canvas_obj.drawCentredString(4.25*inch, 10.5*inch, f"{payload.farmer_details.farmer_name}")
    
    # Timestamp (below farmer name)
    canvas_obj.setFont("Helvetica", 9)
    timestamp = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    canvas_obj.drawCentredString(4.25*inch, 10.2*inch, timestamp)
    
    # Horizontal line separator
    canvas_obj.setLineWidth(1)
    canvas_obj.line(0.5*inch, 10*inch, 8*inch, 10*inch)
    
    canvas_obj.restoreState()
