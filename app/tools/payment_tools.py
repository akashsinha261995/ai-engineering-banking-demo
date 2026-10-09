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


knowledge_tool = {
    "type": "function",
    "function": {
        "name": "search_company_knowledge",
        "description": (
            "Search company policies and support documentation "
            "to answer questions about refunds, payments, "
            "support hours, and company procedures. "
            "Use this tool when the user asks about company policies. "
            "Do not use it for customer account information or payments."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The company policy question to search for."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
}
