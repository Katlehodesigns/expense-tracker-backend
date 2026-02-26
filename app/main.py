from fastapi import FastAPI
from app.api.routes import router as api_router
from app.db.database import engine
from app.models.expense import Base
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def health_check(): return{"status":"ok"}
