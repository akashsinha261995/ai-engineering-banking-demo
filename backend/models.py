from sqlalchemy import Column, Float, String

from backend.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    outstanding = Column(Float, nullable=False)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)