from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models import FinancePayload
from app.services.finance_report_generator import FinanceReportGenerator

router = APIRouter(
    prefix="/api",
    tags=["Finance"]
)


@router.post("/validate-finance")
async def validate_finance(payload: FinancePayload):
    """Validate finance data and calculate totals"""
    print("\n" + "="*50)
    print("📥 RECEIVED PAYLOAD:")
    print("="*50)
    print(f"👤 Farmer: {payload.farmer_details.farmer_name}")
    print(f"🌾 Crop: {payload.farmer_details.crop_name}")
    print(f"📅 Season: {payload.farmer_details.season}")
    print(f"📍 Location: {payload.farmer_details.village}, {payload.farmer_details.district}")
    print(f"\n💰 Expenses ({len(payload.expenses)} items):")
    for idx, exp in enumerate(payload.expenses, 1):
        print(f"  {idx}. {exp.category}: ₹{exp.amount} on {exp.expense_date}")
    print(f"\n💵 Income ({len(payload.income)} items):")
    for idx, inc in enumerate(payload.income, 1):
        print(f"  {idx}. {inc.category}: ₹{inc.amount} on {inc.income_date}")
    
    try:
        total_expenses = sum(item.amount for item in payload.expenses)
        total_income = sum(item.amount for item in payload.income)
        net_profit = total_income - total_expenses
        
        print(f"\n📊 CALCULATION RESULTS:")
        print(f"  Total Expenses: ₹{total_expenses}")
        print(f"  Total Income: ₹{total_income}")
        print(f"  Net Profit: ₹{net_profit}")
        print("="*50 + "\n")
        
        return {
            "status": "valid",
            "total_expenses": total_expenses,
            "total_income": total_income,
            "net_profit": net_profit
        }
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("="*50 + "\n")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-report")
async def generate_report(payload: FinancePayload):
    """Generate and download PDF finance report"""
    print("\n" + "="*50)
    print("📄 GENERATING PDF REPORT")
    print("="*50)
    print(f"👤 Farmer: {payload.farmer_details.farmer_name}")
    print(f"🌾 Crop: {payload.farmer_details.crop_name}")
    
    try:
        # Generate PDF
        generator = FinanceReportGenerator()
        pdf_buffer = generator.generate(payload)
        
        # Create filename
        farmer_name = payload.farmer_details.farmer_name.replace(" ", "_")
        crop_name = payload.farmer_details.crop_name.replace(" ", "_")
        filename = f"Finance_Report_{farmer_name}_{crop_name}.pdf"
        
        print(f"✅ PDF generated successfully: {filename}")
        print("="*50 + "\n")
        
        # Return PDF as downloadable file
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        print(f"\n❌ PDF GENERATION ERROR: {str(e)}")
        print("="*50 + "\n")
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")
