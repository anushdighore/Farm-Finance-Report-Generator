from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from typing import Any


def draw_page_footer(canvas_obj: Canvas, doc: Any) -> None:
    """Draw footer on each page with GramIQ branding"""
    canvas_obj.saveState()
    
    # Footer text
    footer_text = "Proudly maintained accounting with GramIQ"
    
    # Set font and size for footer
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.setFillGray(0.5)  # Gray color for footer
    
    # Draw footer at bottom center
    page_width = 8.27 * inch  # A4 width
    canvas_obj.drawCentredString(page_width / 2, 0.4 * inch, footer_text)
    
    canvas_obj.restoreState()
