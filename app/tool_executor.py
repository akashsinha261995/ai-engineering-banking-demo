import logging
import json
import time

from tool_registry import ( 
    TOOL_FUNCTIONS,
    ALLOWED_TOOLS, 
    TOOL_PERMISSIONS
)

from auth import get_user_role
from models import PaymentToolInput

logger = logging.getLogger(__name__)

def execute_tool(tool_call, request_id, token):

    logger.info(
        "Executing tool",
        extra={
            "event": "tool_execution",
            "tool": tool_call.function.name,
            "request_id": request_id
        }
    )

    print("\nTOOL CALL:")
    print("Function:", tool_call.function.name)
    print("Arguments:", tool_call.function.arguments)

    tool_name = tool_call.function.name

    if tool_name not in ALLOWED_TOOLS:

        logger.warning(
            "Tool rejected",
            extra={
                "event": "tool_rejected",
                "tool": tool_name,
                "request_id": request_id
            }
        )

        return {
            "success": False,
            "error": f"Tool not allowed: {tool_name}"
        }

    user_role = get_user_role(token)

    
    # ---------------------------------------------
    # Find the Python function
    # ---------------------------------------------

    allowed_tools = TOOL_PERMISSIONS.get(user_role, set())

    if tool_name not in allowed_tools:

        logger.warning(
            "Tool rejected",
            extra={
                "event": "tool_rejected",
                "tool": tool_name,
                "request_id": request_id
            }
        )

        return {
            "success": False,
            "error": f"Tool not allowed: {tool_name}"
        }

    tool_function = TOOL_FUNCTIONS.get(tool_name)

    arguments = json.loads(
            tool_call.function.arguments
        )
    


    # ---------------------------------------------
    # Financial action
    # ---------------------------------------------

    if tool_name == "record_payment":

        try:
            payment_input = PaymentToolInput(
                **arguments
            )

        except Exception as e:

            logger.warning(
                "Invalid payment tool arguments",
                extra={
                    "event": "tool_validation_failed",
                    "tool": tool_name,
                    "request_id": request_id
                }
            )

            return {
                "success": False,
                "error": "Invalid payment arguments"
            }

        customer_id = payment_input.customer_id
        amount = payment_input.amount

        print("\nPAYMENT CONFIRMATION")
        print(f"Customer ID: {customer_id}")
        print(f"Amount: ₹{amount}")

        confirmation = input(
            "Confirm payment? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":

            return {
                "success": False,
                "error": "Payment cancelled by user"
            }

        # Start timing only after user confirmation
        start_time = time.perf_counter()

        result = tool_function(
            customer_id,
            amount,
            token
        )

        if hasattr(result, "model_dump"):
            result = result.model_dump()

        # Verify state after successful payment
        if result.get("success") is True:

            verified_balance = TOOL_FUNCTIONS[
                "get_customer_balance"
            ](
                customer_id,
                token
            )

            if hasattr(verified_balance, "model_dump"):
                verified_balance = verified_balance.model_dump()

            result["verified_balance"] = (
                verified_balance
            )

        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

    # ---------------------------------------------
    # Normal read-only tools
    # ---------------------------------------------

    else:

        # Start timing immediately before tool execution
        start_time = time.perf_counter()

        if "customer_id" in arguments:

            customer_id = str(
                arguments["customer_id"]
            )

            result = tool_function(
                customer_id,
                token
            )

        else:

            result = tool_function(
                **arguments
            )

        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )


    # ---------------------------------------------
    # Normalize result
    # ---------------------------------------------

    if hasattr(result, "model_dump"):
        result = result.model_dump()

    if "success" not in result:

        if "error" in result:
            result["success"] = False
        else:
            result["success"] = True

    # ---------------------------------------------
    # Tool execution log
    # ---------------------------------------------

    logger.info(
        "Tool execution completed",
        extra={
            "event": "tool_execution_completed",
            "tool": tool_name,
            "request_id": request_id,
            "duration_ms": duration_ms,
            "success": result["success"]
        }
    )

    return result
