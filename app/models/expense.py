from pydantic imort BaseModel
from datetime import date

class Expense(BaseModle):
    id: int
    description: str
    amount: float
    date:date