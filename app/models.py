from pydantic import BaseModel


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