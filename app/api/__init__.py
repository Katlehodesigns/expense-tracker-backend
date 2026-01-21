from fastapi import APIRouter
from app.api.routes.expense import router as expense_router

router = APIRouter()
router.include_router(expense_router, prefix="/expenses", tags=["expenses"])
