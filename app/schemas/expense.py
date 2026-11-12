from pydantic import BaseModel, Field
from typing import Optional
import datetime


class ExpenseCreate(BaseModel):
    description: str
    amount: float = Field(gt=0)
    date: datetime.date


class ExpenseOut(ExpenseCreate):
    id: int


class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = Field(default=None, gt=0)
    date: Optional[datetime.date] = None