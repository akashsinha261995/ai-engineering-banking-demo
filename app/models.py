from pydantic import BaseModel, Field

class Customer(BaseModel):

    id: str
    name: str
    phone: str
    outstanding: float

class CustomerBalance(BaseModel):

    customer_id: str
    name: str
    outstanding: float

class PaymentResult(BaseModel):

    customer_id: str
    name: str
    payment:float
    remaining_outstanding: float

class PaymentToolInput(BaseModel):

    customer_id: str
    amount: float = Field(gt=0, description="Payment amount must be greater than zero")