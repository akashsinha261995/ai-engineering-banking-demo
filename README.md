# FDE AI Project

This repository contains a small customer support demo that combines an LLM-powered CLI assistant with a FastAPI backend service for customer and payment operations.

## Overview

The project has two main parts:

- A terminal-based AI assistant in `app/` that talks to an LLM and can call tools
- A FastAPI service in `backend/` that exposes customer and payment APIs backed by SQLite

The overall idea is to simulate a customer support workflow where an assistant can check account details and record payments based on natural-language requests.

## Features

- Customer lookup by ID
- Outstanding balance retrieval
- Payment processing with validation
- Payment confirmation flow in the CLI assistant
- SQLite persistence for customer and payment records
- FastAPI endpoints for backend integration

## Project structure

- `app/agent.py` - conversational agent logic and tool-calling flow
- `app/llm.py` - OpenRouter/OpenAI client setup
- `app/main.py` - interactive CLI runner
- `app/tool_registry.py` - maps tool names to functions
- `app/tool_executor.py` - runs tool calls and confirms payment requests
- `app/customer_service.py` - in-memory demo customer data
- `app/tools/` - tool schemas exposed to the LLM
- `backend/main.py` - FastAPI app with customer/payment endpoints
- `backend/database.py` - SQLAlchemy database configuration
- `backend/models.py` - SQLAlchemy models for customers and payments
- `backend/schemas.py` - request/response validation models
- `backend/init_db.py` - creates the SQLite database and seed data
- `customers.db` - local SQLite database
- `requirements.txt` - Python dependencies
- `tests/` - test folder

## Backend API

The API is created in `backend/main.py` and exposes these routes:

- `GET /customers/{customer_id}`
  - Returns customer information
- `GET /customers/{customer_id}/balance`
  - Returns the customer's outstanding balance
- `POST /customers/{customer_id}/payments`
  - Records a payment for a customer

The payment route validates:

- customer exists
- payment amount is greater than zero
- payment does not exceed the outstanding balance

## Database model

The database stores:

- `Customer`
  - `id`
  - `name`
  - `phone`
  - `outstanding`
- `Payment`
  - `id`
  - `customer_id`
  - `amount`

Seed data is added automatically by `backend/init_db.py` for customers 101, 102, and 103.

## CLI assistant flow

The CLI app in `app/main.py` starts a loop that asks for user input and calls the LLM. The assistant can:

1. Accept a natural-language request from the user
2. Decide whether a tool is needed
3. Execute a Python tool for customer lookup or payment logic
4. Send the result back to the model
5. Return the final response to the user

The payment flow includes explicit confirmation before processing a financial action.

## Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set environment variables

```bash
export OPENROUTER_API_KEY="your_api_key_here"
```

PowerShell:

```powershell
$env:OPENROUTER_API_KEY="your_api_key_here"
```

### Run the backend API

```bash
uvicorn backend.main:app --reload
```

### Run the CLI app

```bash
python app/main.py
```

## Example usage

```text
You: Get customer 101

You: What is the outstanding balance for customer 102?

You: Record a payment of 500 for customer 101
```

For payment requests, the CLI prompts for confirmation before the payment is recorded.

## Notes

- The customer data in `app/customer_service.py` is demo-only and kept in memory.
- The backend database is SQLite and persists to `customers.db`.
- The app uses the OpenRouter API via `app/llm.py` and the model is configured as `openrouter/free`.
- This project is a demo/prototype and not a production-ready financial system.
