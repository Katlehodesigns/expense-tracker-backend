from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.expense import ExpenseCreate, ExpenseOut, ExpenseUpdate
from app.models.expense import Expense
from app.db.debs import get_db

print(" expense.py LOADED")

router = APIRouter()

@router.post("/", response_model=ExpenseOut)
def create_expense(
    expense: ExpenseCreate, 
    db: Session = Depends(get_db)
    
):
    new_expense = Expense(
        description = expense.description,
        amount=expense.amount,
        date = expense.date
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get("/", response_model=list[ExpenseOut])
def list_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"status": "deleted"}

@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
):
    db_expense = db.get(Expense, expense_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    update_data = expense.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_expense, field, value)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(db_expense)
    return db_expense

print("PATCH DECORATOR REACHED")

@router.patch("/{expense_id}")
def patch_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db)
):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense.description is not None:
        db_expense.description = expense.description
    if expense.amount is not None:
        db_expense.amount = expense.amount
    if expense.date is not None:
        db_expense.date = expense.date

    update_data = expense.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_expense, field, value)


    db.commit()
    db.refresh(db_expense)
    return db_expense
