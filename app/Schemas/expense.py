from pydantic import BaseModel
from typing import Optional
import datetime


class ExpenseCreate(BaseModel):
    description: str
    amount: float
    date: datetime.date


class ExpenseOut(ExpenseCreate):
    id: int


class ExpenseUpdate(BaseModel):
    description: str | None= None
    amount: float |None = None
    date: datetime.date | None = None