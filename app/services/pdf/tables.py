from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from app.services.pdf.styles import get_transaction_table_style


def farmer_table(payload):
    data = [
        ["Farmer Name:", payload.farmer_details.farmer_name],
        ["Crop Name:", payload.farmer_details.crop_name],
        ["Season:", payload.farmer_details.season],
        ["Total Acres:", f"{payload.farmer_details.total_acres} acres"],
        ["Sowing Date:", str(payload.farmer_details.sowing_date)],
        ["Harvest Date:", str(payload.farmer_details.harvest_date)],
        ["Location:", f"{payload.farmer_details.village}, {payload.farmer_details.taluka}"],
        ["District:", payload.farmer_details.district],
        ["State:", payload.farmer_details.state],
    ]

    table = Table(data, colWidths=[2 * inch, 4 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#dbeafe")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.grey),
                ("LINEBELOW", (0, -1), (-1, -1), 1, colors.grey),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f0f9ff")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return table


def expense_table(expenses):
    data = [["#", "Category", "Amount", "Date", "Description"]]
    total = 0

    for idx, expense in enumerate(expenses, 1):
        data.append(
            [
                str(idx),
                expense.category,
                f"{expense.amount:,.2f}",
                str(expense.expense_date),
                expense.description or "-",
            ]
        )
        total += expense.amount

    data.append(["", "Total Expenses", f"{total:,.2f}", "", ""])

    table = Table(data, colWidths=[0.5 * inch, 1.5 * inch, 1.3 * inch, 1.2 * inch, 2 * inch])
    table.setStyle(get_transaction_table_style())
    return table, total


def income_table(incomes):
    data = [["#", "Category", "Amount", "Date", "Description"]]
    total = 0

    for idx, income in enumerate(incomes, 1):
        data.append(
            [
                str(idx),
                income.category,
                f"{income.amount:,.2f}",
                str(income.income_date),
                income.description or "-",
            ]
        )
        total += income.amount

    data.append(["", "Total Income", f"{total:,.2f}", "", ""])

    table = Table(data, colWidths=[0.5 * inch, 1.5 * inch, 1.3 * inch, 1.2 * inch, 2 * inch])
    table.setStyle(get_transaction_table_style())
    return table, total


def finance_summary_section(total_income, total_expenses, total_acres, total_production=0):
    """Create detailed finance summary section with calculations"""
    cost_per_acre = total_expenses / total_acres if total_acres > 0 else 0
    net_profit = total_income - total_expenses
    profit_status = "Profit" if net_profit >= 0 else "Loss"
    profit_color = colors.HexColor("#16a34a") if net_profit >= 0 else colors.HexColor("#dc2626")

    data = [
        ["Total Income:", f"{total_income:,.2f}"],
        ["Total Expense:", f"{total_expenses:,.2f}"],
        [f"{profit_status}:", f"{abs(net_profit):,.2f}"],
        ["Cost of Cultivation/Acre:", f"{cost_per_acre:,.2f}"],
    ]

    table = Table(data, colWidths=[3 * inch, 2.5 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e0e7ff")),
                ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#f5f3ff")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("LINEBELOW", (0, 0), (-1, -2), 1, colors.grey),
                ("LINEBELOW", (0, -1), (-1, -1), 1, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 15),
                ("RIGHTPADDING", (0, 0), (-1, -1), 15),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                # Highlight profit/loss row
                ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#fff0f5")) if net_profit < 0 else ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#f0fff4")),
                ("TEXTCOLOR", (1, 3), (1, 3), profit_color),
            ]
        )
    )
    return table


def ledger_table(expenses, incomes):
    """Create merged ledger table of all transactions (expenses and income)"""
    # Create transaction list with type
    transactions = []
    
    # Add expenses
    for expense in expenses:
        transactions.append({
            'date': str(expense.expense_date),
            'particulars': expense.category,
            'type': 'Expense',
            'description': expense.description or '-',
            'amount': expense.amount
        })
    
    # Add incomes
    for income in incomes:
        transactions.append({
            'date': str(income.income_date),
            'particulars': income.category,
            'type': 'Income',
            'description': income.description or '-',
            'amount': income.amount
        })
    
    # Sort by date
    transactions.sort(key=lambda x: x['date'])
    
    # Create table data with headers
    data = [["Date", "Particulars", "Transaction Type", "Description", "Amount"]]
    
    for txn in transactions:
        data.append([
            txn['date'],
            txn['particulars'],
            txn['type'],
            txn['description'],
            f"{txn['amount']:,.2f}"
        ])
    
    table = Table(data, colWidths=[1.2 * inch, 1.4 * inch, 1.3 * inch, 1.5 * inch, 1.2 * inch])
    table.setStyle(get_transaction_table_style())
    return table
