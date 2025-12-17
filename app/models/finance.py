from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class ExpenseItem(BaseModel):
    """Individual expense entry"""
    category: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)
    expense_date: date
    description: Optional[str] = Field(None, max_length=200)


class IncomeItem(BaseModel):
    """Individual income entry"""
    category: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)
    income_date: date
    description: Optional[str] = Field(None, max_length=200)
