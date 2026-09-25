import httpx
import uuid

from models import (
    Customer,
    CustomerBalance,
    PaymentResult
)


def get_customer(customer_id: str):
    try:
        response = httpx.get(
            f"http://127.0.0.1:8000/customers/{customer_id}",
            timeout=5.0
        )

        if response.status_code == 404:
            return {"error": "Customer not found"}

        response.raise_for_status()

        data = response.json()

        return Customer(
            id=data["id"],
            name=data["name"],
            phone=data["phone"],
            outstanding=data["outstanding"]
        )

    except httpx.ConnectError:
        return {
            "error": "Customer service is currently unavailable"
        }

    except httpx.TimeoutException:
        return {
            "error": "Customer service request timed out"
        }

    except httpx.HTTPStatusError:
        return {
            "error": "Customer service returned an error"
        }


def get_customer_balance(customer_id: str):
    try:
        response = httpx.get(
            f"http://127.0.0.1:8000/customers/{customer_id}/balance",
            timeout=5.0
        )

        if response.status_code == 404:
            return {"error": "Customer not found"}

        response.raise_for_status()

        data = response.json()

        return CustomerBalance(
            customer_id=data["customer_id"],
            name=data["name"],
            outstanding=data["outstanding"]
        )

    except httpx.ConnectError:
        return {
            "error": "Customer service is currently unavailable"
        }

    except httpx.TimeoutException:
        return {
            "error": "Customer service request timed out"
        }

    except httpx.HTTPStatusError:
        return {
            "error": "Customer service returned an error"
        }


def record_payment(customer_id: str, amount: float):
    payment_id = str(uuid.uuid4())
    try:
        response = httpx.post(
            f"http://127.0.0.1:8000/customers/{customer_id}/payments",
            json={"payment_id": payment_id, "amount": amount},
            timeout=5.0
        )

        if response.status_code == 404:
            return {
                "error": "Customer not found"
            }

        if response.status_code == 400:
            return {
                "error": response.json()["detail"]
            }

        response.raise_for_status()

        data = response.json()

        return PaymentResult(
            customer_id=data["customer_id"],
            name=data["name"],
            payment=data["payment"],
            remaining_outstanding=data["remaining_outstanding"]
        )

    except httpx.ConnectError:
        return {
            "error": "Customer service is currently unavailable. Payment status is unknown."
        }

    except httpx.TimeoutException:
        return {
            "error": "Payment request timed out. Payment status is unknown."
        }

    except httpx.HTTPStatusError:
        return {
            "error": "Customer service returned an error. Payment status is unknown."
        }