from fastapi import FastAPI
from app.api.routes import router
from app.db.database import engine
from app.models import expense

expense.Base.metadata.create_all(bind=engine)
app = FastAPI(title = "Expense Tracker Api")
app.include_router(router)
@app.get("/")
def health_check(): return{"status":"ok"}
