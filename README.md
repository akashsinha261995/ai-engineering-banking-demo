# FDE AI Project

This repository is a customer support prototype that combines a terminal-based AI assistant, a FastAPI backend, and a Chroma-backed retrieval layer for company policy lookup.

## Overview

The system supports two main use cases:

- answering support and policy questions using retrieved company knowledge
- looking up customer account details and handling payments through an authenticated backend service

It uses LLM tool calling, HTTP client requests to the backend, and retrieval-augmented generation to respond with grounded answers.

## Components

### 1. CLI assistant
- entry point: app/main.py
- main logic: app/agent.py
- prompts the user for input and a bearer token
- can call tools for customer lookup, balance lookup, payment creation, and policy search

### 2. FastAPI backend
- entry point: backend/main.py
- handles customer and payment APIs
- validates JWT tokens
- enforces role checks for sensitive actions
- stores data in SQLite

### 3. RAG layer
- source content: knowledge/company_policies.txt
- chunking: app/chunker.py
- embeddings: app/embeddings.py
- vector store: app/chroma_store.py
- retrieval tool: app/knowledge_tool.py
- evaluation script: tests/rag_eval.py

## Project structure

- app/agent.py - conversation loop and tool calling
- app/main.py - CLI app entry
- app/llm.py - OpenAI/OpenRouter request wrapper
- app/config.py - required environment variables
- app/auth.py - JWT role helper used by the client
- app/customer_service.py - HTTP client that calls the backend
- app/tool_executor.py - executes tool calls and confirms payment requests
- app/tool_registry.py - registers available tools
- app/tools/__init__.py - exports tool schemas
- app/tools/customer_tools.py - customer and balance tools
- app/tools/payment_tools.py - payment and knowledge tools
- app/chroma_store.py - Chroma vector database access
- app/vector_store.py - older in-memory vector store implementation
- app/knowledge.py - fallback keyword search
- app/knowledge_tool.py - policy search wrapper used by the agent
- app/chunker.py - splits policy text into document chunks
- app/embeddings.py - embedding generation
- backend/main.py - FastAPI app
- backend/auth.py - login and registration routes
- backend/security.py - JWT issuance, password hashing, role checks
- backend/database.py - SQLAlchemy database setup
- backend/models.py - Customer, Payment, and User schemas
- backend/init_db.py - database initialization and sample data
- backend/schemas.py - Pydantic request/response models
- knowledge/company_policies.txt - policy knowledge base
- customers.db - SQLite database
- tests/rag_eval.py - retrieval and answer evaluation
- requirements.txt - dependency list

## Features

- policy lookup through Chroma vector search
- grounded answer generation with source-aware context
- customer lookup by ID
- outstanding balance retrieval
- payment processing with validation
- confirmation step before making a payment in the CLI
- JWT-based authentication for protected backend endpoints
- admin-role enforcement for payment actions

## API routes

The backend exposes these endpoints:

- POST /auth/register
- POST /auth/login
- GET /customers/{customer_id}
- GET /customers/{customer_id}/balance
- POST /customers/{customer_id}/payments

Notes:

- customer read endpoints require a bearer token
- payment creation requires the admin role
- the backend validates amount, customer existence, and outstanding balance before updating records

## RAG workflow

The policy retrieval workflow is:

1. knowledge text is split into chunks
2. embeddings are created for each chunk
3. chunks are stored in a local Chroma collection
4. a question is embedded and compared to stored vectors
5. relevant policy text is added to the LLM context

The agent also stores source metadata and appends source references when relevant company policy results are used.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a .env file in the project root:

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

Run the CLI in another terminal:

```bash
python app/main.py
```

## Seed data

The backend creates demo customers at startup:

- 101 - Rahul Kumar
- 102 - Priya Sharma
- 103 - Amit Singh

## Evaluation

The project includes a retrieval-evaluation script at tests/rag_eval.py.

It checks:

- whether the expected policy section is retrieved
- whether the final answer contains expected keywords
- whether unsupported questions return no relevant result

## Notes

- This is a prototype/demo and is not a production-ready financial system.
- The knowledge layer uses local company documents and a local Chroma vector store.
- The assistant and backend are intended to work together through authenticated HTTP calls.
