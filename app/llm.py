import os
import logging
import time

from openai import OpenAI

from config import (
    OPENROUTER_API_KEY, 
    OPENROUTER_MODEL, 
    OPENROUTER_BASE_URL
)

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)


def ask_llm(
    messages: list[dict],
    tools: list[dict] | None = None,
    request_id: str | None = None
):

    request = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
    }

    if tools:
        request["tools"] = tools
        request["tool_choice"] = "auto"

    start_time = time.perf_counter()

    response = client.chat.completions.create(**request)

    duration_ms = round(
        (time.perf_counter() - start_time) * 1000,
        2
    )

    logger.info(
        "LLM request completed",
        extra={
            "event": "llm_request",
            "request_id": request_id,
            "duration_ms": duration_ms
        }
    )

    return response
