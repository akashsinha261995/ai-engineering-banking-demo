from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from backend.models import (
    Customer, Payment
)
from backend.database import Base, engine, get_db
from backend.init_db import init_db
from backend.schemas import (
    CustomerBalanceResponse,
    CustomerResponse,
    PaymentRequest,
    PaymentResponse,
)

app = FastAPI(title="Customer Service API")

init_db()  # Initialize the database and create tables if they don't exist

@app.get(
        "/customers/{customer_id}",
        response_model=CustomerResponse,
)
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    customer = db.get(Customer, customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "outstanding": customer.outstanding
    }

@app.get(
        "/customers/{customer_id}/balance",
        response_model=CustomerBalanceResponse
)
def get_customer_balance(
    customer_id: str,
    db: Session = Depends(get_db)
):
    customer = db.get(Customer, customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "customer_id": customer.id,
        "name": customer.name,
        "outstanding": customer.outstanding
    }

@app.post(
    "/customers/{customer_id}/payments",
    response_model=PaymentResponse
)
def record_payment(
    customer_id: str,
    payment: PaymentRequest,
    db: Session = Depends(get_db)
):
    existing_payment = db.get(Payment, payment.payment_id)

    if existing_payment:
        customer = db.get(Customer, existing_payment.customer_id)

        return {
            "customer_id": customer.id,
            "name": customer.name,
            "payment": existing_payment.amount,
            "remaining_outstanding": customer.outstanding
        }

    customer = db.get(Customer, customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if payment.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Payment amount must be greater than zero"
        )

    if payment.amount > customer.outstanding:
        raise HTTPException(
            status_code=400,
            detail="Payment cannot exceed the outstanding balance"
        )

    try:

        customer.outstanding -= payment.amount

        new_payment = Payment(
            id=payment.payment_id,
            customer_id=customer.id,
            amount=payment.amount
        )

        db.add(new_payment)

        db.commit()
        db.refresh(customer)

    except Exception:
        db.rollback()
        raise

    return {
        "customer_id": customer.id,
        "name": customer.name,
        "payment": payment.amount,
        "remaining_outstanding": customer.outstanding
    }