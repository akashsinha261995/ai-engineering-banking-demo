from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):
    payment_id: str
    amount: float = Field(gt=0)


class CustomerResponse(BaseModel):
    id: str
    name: str
    phone: str
    outstanding: float


class CustomerBalanceResponse(BaseModel):
    customer_id: str
    name: str
    outstanding: float


class PaymentResponse(BaseModel):
    customer_id: str
    name: str
    payment: float
    remaining_outstanding: float