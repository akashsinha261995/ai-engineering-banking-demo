customer_tool = {
    "type": "function",
    "function": {
        "name": "get_customer",
        "description": "Get customer information using the customer ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The ID of the customer."
                }
            },
            "required": ["customer_id"],
            "additionalProperties": False
        }
    }
}


balance_tool = {
    "type": "function",
    "function": {
        "name": "get_customer_balance",
        "description": "Get the outstanding balance of a customer using the customer ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The ID of the customer."
                }
            },
            "required": ["customer_id"],
            "additionalProperties": False
        }
    }
}