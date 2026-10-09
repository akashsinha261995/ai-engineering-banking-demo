import logging
import json
import uuid
import time

logger = logging.getLogger(__name__)

from llm import ask_llm

from tools import (
    customer_tool,
    balance_tool,
    payment_tool,
    knowledge_tool
)

from tool_executor import execute_tool

TOOLS = [
    customer_tool,
    balance_tool,
    payment_tool,
    knowledge_tool
]


class CustomerAgent:

    def __init__(self):

        self.messages = [
            {
                "role": "system",
                "content": """
You are a customer support assistant.

You can retrieve customer information, perform customer
operations, and search company policies using the available tools.

When the user asks about company policies, refunds, payment
rules, support hours, or company procedures, use the
search_company_knowledge tool.

When responding after a tool call, use only information
returned by the tool.

Never introduce information from previous customers
or previous tool calls unless it is directly relevant
to the current request.

If a tool returns an error, clearly report that error
and do not guess or substitute information.

Do not invent customer information.

For requests requiring multiple actions, perform the
actions sequentially.

Use only one tool call at a time. After receiving the
result of a tool call, decide whether another tool is
needed.

For financial actions such as recording a payment,
do not ask the user for confirmation yourself.
The application handles confirmation before executing
the financial action.

If a financial action is cancelled by the user, do not
retry it unless the user explicitly asks again. Only provide
current balance when enquired about it. Don't add or provide any
pleasant messages or greetings. Only provide the information requested.

After a successful state-changing operation, use
another tool to verify the resulting state when
appropriate.

When using search_company_knowledge:
- Answer using the retrieved policy content.
- Include the source filename and section from the tool result.
- Do not invent or modify source metadata.
- If no relevant policy is found, clearly say that you could not find the answer 
  in the company knowledge base.

"""
            }
        ]

    def run(self, user_input, token):
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        retrieved_sources = []

        logger.info(
            "Received user request",
            extra={
                "event": "request_received",
                "request_id": request_id
            }
        )

        self.messages.append({
            "role": "user",
            "content": user_input
        })

        while True:

            response = ask_llm(
                self.messages,
                tools=TOOLS,
                request_id=request_id
            )

            message = response.choices[0].message

            # print(
            #     "\nRAW LLM RESPONSE:",
            #     message
            # )

            # No tool call = final answer
            if not message.tool_calls:

                answer = message.content or ""

                if retrieved_sources:
                    source_lines = [
                        f"- {source} — {section}"
                        for source, section in retrieved_sources
                    ]

                    answer += "\n\nSources:\n" + "\n".join(source_lines)
                

                self.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                duration_ms = round(
                    (time.perf_counter() - start_time) * 1000, 2)

                logger.info(
                    "Request completed",
                    extra={
                        "event": "request_completed",
                        "request_id": request_id,
                        "duration_ms": duration_ms
                    }
                )

                return answer

            # Process only one tool call
            tool_call = message.tool_calls[0]

            logger.info(
                "Tool requested",
                extra={
                    "event": "tool_call",
                    "tool": tool_call.function.name,
                    "request_id": request_id
                }
            )

            self.messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": (
                                tool_call.function.arguments
                            )
                        }
                    }
                ]
            })

            # Execute tool
            result = execute_tool(
                tool_call,
                request_id,
                token
            )

            if (
                tool_call.function.name == "search_company_knowledge"
                and result.get("success")
                and result.get("found")
            ):
                for match in result.get("matches", []):
                    source_info = (
                        match["source"],
                        match["section"]
                    )

                    if source_info not in retrieved_sources:
                        retrieved_sources.append(source_info)


            # Send tool result back to LLM
            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })