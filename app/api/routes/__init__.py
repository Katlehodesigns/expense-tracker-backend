from fastapi import APIRouter
from app.api.routes.expense import router as expense_router
from app.api.routes.auth import router as auth_router

router = APIRouter()
router.include_router(expense_router, prefix="/expenses", tags=["expenses"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])