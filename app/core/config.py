from pydantic import BaseSettings

class Setting(BaseSettings): app_name: str = "Expense Tracker Api"

settings = Settings()