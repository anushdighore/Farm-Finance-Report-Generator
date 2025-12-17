from pydantic import BaseModel, Field
from typing import List
from .farmer import FarmerDetails
from .finance import ExpenseItem, IncomeItem


class FinancePayload(BaseModel):
    """Complete finance submission"""
    farmer_details: FarmerDetails
    expenses: List[ExpenseItem] = Field(..., min_length=1)
    income: List[IncomeItem] = Field(..., min_length=1)
