from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime


class Expense(Base):
    __tablename__="expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

user_id = Column(Integer, ForeignKey("users.id"))
user = relationship("User")
