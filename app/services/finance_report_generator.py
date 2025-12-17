from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from app.models import FinancePayload
from app.services.pdf.styles import build_styles
from app.services.pdf.tables import farmer_table, expense_table, income_table, finance_summary_section, ledger_table
from app.services.pdf.header import draw_page_header
from app.services.pdf.footer import draw_page_footer
from app.services.pdf.chart import generate_income_expense_chart


class FinanceReportGenerator:
    """Generate the finance PDF report with headers on every page."""

    def __init__(self):
        self.styles = build_styles()

    def generate(self, payload: FinancePayload) -> BytesIO:
        buffer = BytesIO()
        
        # Header and footer function for every page
        def on_page(canvas, doc):
            draw_page_header(canvas, doc, payload, doc.page)
            draw_page_footer(canvas, doc)
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=120,  # More space for header
            bottomMargin=50,
            title=f"Farm Finance Report - {payload.farmer_details.farmer_name}",
        )

        elements = []

        # Finance Summary Section (FIRST - before farmer details)
        elements.append(Paragraph("📈 Finance Summary", self.styles["SectionHeader"]))
        total_expenses_calc = sum(item.amount for item in payload.expenses)
        total_income_calc = sum(item.amount for item in payload.income)
        finance_summary_tbl = finance_summary_section(
            total_income=total_income_calc,
            total_expenses=total_expenses_calc,
            total_acres=payload.farmer_details.total_acres,
            total_production=0  # Add production data if available
        )
        elements.append(finance_summary_tbl)
        elements.append(Spacer(1, 0.5 * inch))

        # Generate and embed chart
        chart_buffer = generate_income_expense_chart(total_income_calc, total_expenses_calc)
        chart_image = Image(chart_buffer, width=5.5*inch, height=2.75*inch)
        elements.append(chart_image)
        elements.append(Spacer(1, 0.4 * inch))

        # Expenses
        elements.append(Paragraph("💰 Expenses", self.styles["SectionHeader"]))
        expense_tbl, total_expenses = expense_table(payload.expenses)
        elements.append(expense_tbl)
        elements.append(Spacer(1, 0.4 * inch))

        # Income
        elements.append(Paragraph("💵 Income", self.styles["SectionHeader"]))
        income_tbl, total_income = income_table(payload.income)
        elements.append(income_tbl)
        elements.append(Spacer(1, 0.4 * inch))

        # Ledger
        elements.append(Paragraph("📝 Ledger", self.styles["SectionHeader"]))
        ledger_tbl = ledger_table(payload.expenses, payload.income)
        elements.append(ledger_tbl)
        elements.append(Spacer(1, 0.4 * inch))

        # Farmer section (after expenses and income)
        elements.append(Paragraph("📋 Farmer & Crop Details", self.styles["SectionHeader"]))
        elements.append(farmer_table(payload))
        elements.append(Spacer(1, 0.5 * inch))

        # Footer
        elements.append(Spacer(1, 0.5 * inch))
        footer_text = f"Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        elements.append(Paragraph(footer_text, self.styles["InfoText"]))

        # Build with header on every page
        doc.build(elements, onFirstPage=on_page, onLaterPages=on_page)
        buffer.seek(0)
        return buffer
