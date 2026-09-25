payment_tool = {
    "type": "function",
    "function": {
        "name": "record_payment",
        "description": "Record a payment made by a customer and update their outstanding balance.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The ID of the customer making the payment."
                },
                "amount": {
                    "type": "number",
                    "description": "The payment amount."
                }
            },
            "required": ["customer_id", "amount"],
            "additionalProperties": False
        }
    }
}