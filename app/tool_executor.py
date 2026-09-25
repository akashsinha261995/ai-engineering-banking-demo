import logging
import json
import time

from tool_registry import TOOL_FUNCTIONS


logger = logging.getLogger(__name__)


def execute_tool(tool_call, request_id):

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

    arguments = json.loads(
        tool_call.function.arguments
    )

    # ---------------------------------------------
    # Find the Python function
    # ---------------------------------------------

    tool_function = TOOL_FUNCTIONS.get(tool_name)

    if tool_function is None:

        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    # ---------------------------------------------
    # Financial action
    # ---------------------------------------------

    if tool_name == "record_payment":

        customer_id = str(
            arguments["customer_id"]
        )

        amount = float(
            arguments["amount"]
        )

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
            amount
        )

        if hasattr(result, "model_dump"):
            result = result.model_dump()

        # Verify state after successful payment
        if result.get("success") is True:

            verified_balance = TOOL_FUNCTIONS[
                "get_customer_balance"
            ](
                customer_id
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
                customer_id
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
