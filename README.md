# Farm Finance Report Generator

A FastAPI-based application that generates professional PDF financial reports for farmers. The system collects farm details, expenses, and income, then generates comprehensive reports with charts, ledgers, and financial summaries.

## Features

- **Finance Summary**: Calculates total income, expenses, and cost of cultivation per acre
- **Income vs Expense Chart**: Visual bar chart showing income vs expense comparison
- **Transaction Ledger**: Merged table of all income and expense transactions sorted by date
- **Professional PDF Output**: Multi-page PDF with headers and footers on every page
- **Responsive Forms**: HTML/CSS/JavaScript frontend for data collection
- **Data Validation**: Pydantic-based backend validation with detailed error handling

## Setup Instructions

### Prerequisites

- Python 3.8+
- Windows/Mac/Linux

### Installation

1. **Clone the repository** (or extract the project folder)
   ```bash
   cd "d:\4_Gramiq\Finance Report Generator for Farmers using FASTAPI Backend"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Application

1. **Ensure virtual environment is activated** (see Setup step 3)

2. **Start the FastAPI server**
   ```bash
   uvicorn app.main:app --reload
   ```
   - Server will run at: `http://127.0.0.1:8000`
   - Auto-reload enabled for development

3. **Open in browser**
   - Navigate to: `http://127.0.0.1:8000`
   - Fill in the farm details, expenses, and income
   - Click "Generate Report" to download the PDF

## Libraries Used

### Backend
- **FastAPI** - Modern Python web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **Pydantic** - Data validation using Python type hints
- **Python-multipart** - Handle multipart form data

### PDF Generation
- **ReportLab** - Create professional PDF documents programmatically
- **Matplotlib** - Generate charts and visualizations

### Frontend
- **HTML5/CSS3** - Form interface and styling
- **Vanilla JavaScript** - Form submission and PDF download handling
- **Fetch API** - Communicate with backend endpoints

## Project Structure

```
Finance Report Generator/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── farmer.py          # Farmer details model
│   │   ├── finance.py         # Expense and Income models
│   │   └── payload.py         # Request payload model
│   ├── routers/
│   │   ├── __init__.py
│   │   └── finance.py         # API endpoints
│   └── services/
│       ├── __init__.py
│       ├── finance_report_generator.py  # PDF generation orchestration
│       └── pdf/
│           ├── __init__.py
│           ├── styles.py      # PDF styling and paragraph styles
│           ├── tables.py      # Table generation functions
│           ├── header.py      # Page headers
│           ├── footer.py      # Page footers
│           └── chart.py       # Chart generation
├── static/
│   ├── main.js               # Frontend logic
│   └── style.css             # Frontend styling
├── templates/
│   └── home.html             # HTML form
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
└── README.md                 # This file
```

## API Endpoints

### POST `/api/validate-finance`
Validates farmer and finance data without generating PDF.

**Request Body:**
```json
{
  "farmer_details": {
    "farmer_name": "John Doe",
    "crop_name": "Wheat",
    "season": "Kharif",
    "total_acres": 5,
    "sowing_date": "2025-05-15",
    "harvest_date": "2025-10-15",
    "village": "Village Name",
    "taluka": "Taluka Name",
    "district": "District Name",
    "state": "State Name"
  },
  "expenses": [
    {
      "category": "Fertilizers",
      "amount": 1500,
      "expense_date": "2025-06-01",
      "description": "Bought XYZ fertilizer"
    }
  ],
  "income": [
    {
      "category": "Main Crop",
      "amount": 25000,
      "income_date": "2025-11-01",
      "description": "Crop sale"
    }
  ]
}
```

### POST `/api/generate-report`
Generates and returns PDF report.

**Response:** Binary PDF file

## PDF Report Sections

1. **Finance Summary** - Total income, expenses, profit/loss, cost per acre
2. **Income vs Expense Chart** - Visual comparison with light color scheme
3. **Expenses Table** - All expenses with category, amount, date, description
4. **Income Table** - All income entries with category, amount, date, description
5. **Ledger** - Merged transaction list sorted by date (Income and Expense combined)
6. **Farmer & Crop Details** - Complete farmer information

## Features

- ✅ Multi-page PDF with consistent headers and footers
- ✅ Professional styling with color-coded sections
- ✅ Dynamic financial calculations
- ✅ Chart visualization with Matplotlib
- ✅ Transaction ledger with date sorting
- ✅ Real-time form validation
- ✅ Error handling with detailed messages
- ✅ Responsive design

## Troubleshooting

### Port 8000 already in use
```bash
uvicorn app.main:app --reload --port 8001
```

### Module not found errors
Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### PDF not downloading
Check browser console (F12) for errors. Ensure backend is running and accessible.

## Development Notes

- **Frontend validation** prevents invalid data submission
- **Backend validation** (Pydantic) provides additional security
- **PDF generation** is memory-based (no disk saves)
- **Headers/footers** appear on every page automatically
- **Charts** are embedded as PNG images in the PDF

## Support

For issues or questions, check the console output from the FastAPI server for detailed error messages.
