from customer_service import (
    get_customer,
    get_customer_balance,
    record_payment
)

from knowledge_tool import search_company_knowledge

TOOL_PERMISSIONS = {
    "user": {
        "get_customer",
        "get_customer_balance",
        "search_company_knowledge"
    },
    "admin": {
        "get_customer",
        "get_customer_balance",
        "record_payment",
        "search_company_knowledge"
    },
}


TOOL_FUNCTIONS = {
    "get_customer": get_customer,
    "get_customer_balance": get_customer_balance,
    "record_payment": record_payment,
    "search_company_knowledge": search_company_knowledge
}

ALLOWED_TOOLS = set(TOOL_FUNCTIONS.keys())