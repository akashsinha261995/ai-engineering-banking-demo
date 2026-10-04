# FDE AI Project

This project is a customer support demo that combines a terminal AI assistant, a FastAPI backend, and a retrieval-augmented generation (RAG) layer for policy lookup.

## Overview

The system is designed to help with two kinds of tasks:

- answering policy and support questions using retrieved company knowledge
- checking customer account details and recording payments through a backend service

The application uses LLM tool calling, HTTP-based customer service calls, and a local Chroma vector store to ground responses in retrieved context.

## Core components

1. CLI assistant
   - entry point: `app/main.py`
   - uses the `CustomerAgent` in `app/agent.py`
   - prompts for a user token and then calls the backend for customer data and payments

2. FastAPI backend
   - entry point: `backend/main.py`
   - exposes customer and payment endpoints
   - handles JWT authentication and role checks
   - stores state in SQLite

3. RAG layer
   - policy source: `knowledge/company_policies.txt`
   - embedding generation: `app/embeddings.py`
   - chunking: `app/chunker.py`
   - vector retrieval: `app/chroma_store.py`
   - evaluation script: `tests/rag_eval.py`

## Project structure

- `app/agent.py` - LLM conversation loop and tool-calling orchestration
- `app/main.py` - CLI runner
- `app/llm.py` - OpenRouter/OpenAI client wrapper
- `app/config.py` - runtime environment config
- `app/auth.py` - JWT role helper for the client
- `app/customer_service.py` - HTTP client to backend customer endpoints
- `app/tool_executor.py` - tool execution and payment confirmation
- `app/tool_registry.py` - mapping of tool names to functions
- `app/chroma_store.py` - Chroma-backed retrieval implementation
- `app/vector_store.py` - older in-memory vector store alternative
- `app/embeddings.py` - embedding generation
- `app/chunker.py` - splitting source knowledge into chunks
- `app/knowledge.py` - keyword-based knowledge search fallback
- `knowledge/company_policies.txt` - policy content used by the retrieval layer
- `backend/main.py` - FastAPI app
- `backend/auth.py` - register/login routes
- `backend/security.py` - password hashing, JWT creation, validation, and role checks
- `backend/database.py` - SQLAlchemy database config
- `backend/models.py` - customer/payment/user models
- `backend/init_db.py` - DB initialization and seed data
- `backend/schemas.py` - request/response models
- `customers.db` - SQLite database file
- `tests/rag_eval.py` - RAG evaluation script with expected retrieval and answer checks

## Features

- company policy lookup through Chroma vector search
- support-agent style question answering grounded in retrieved context
- customer lookup by ID
- outstanding balance retrieval
- payment recording with validation and confirmation
- JWT-based auth and role checks for protected endpoints

## API routes

The backend exposes:

- `POST /auth/register`
- `POST /auth/login`
- `GET /customers/{customer_id}`
- `GET /customers/{customer_id}/balance`
- `POST /customers/{customer_id}/payments`

Notes:

- customer read endpoints require a bearer token
- payment creation requires the `admin` role
- all payment validation is enforced in the backend before updating the balance

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL=your_model
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
JWT_SECRET=your_jwt_secret
```

Start the backend:

```bash
uvicorn backend.main:app --reload
```

Run the assistant in a separate terminal:

```bash
python app/main.py
```

## RAG evaluation

The repository includes a lightweight retrieval evaluation script in `tests/rag_eval.py`.

It tests questions such as:

- refund timing
- payment escalation rules
- support hours
- whether a payment can exceed the outstanding balance
- employee policy questions that should not have a matching support document

The script checks:

- whether the expected policy section was retrieved
- whether the answer contains the expected keywords
- whether unsupported questions return no relevant retrieval

## Seed data

The application initializes sample customers when the backend starts:

- 101 - Rahul Kumar
- 102 - Priya Sharma
- 103 - Amit Singh

## Notes

- This is a demo/prototype project, not a production-ready financial system.
- The RAG layer uses local policy documents and a local Chroma vector store.
- The CLI and backend are designed to work together through authenticated HTTP calls.
