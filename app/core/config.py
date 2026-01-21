from pydantic import BaseSettings

class Settings(BaseSettings): app_name: str = "Expense Tracker Api"

settings = Settings()