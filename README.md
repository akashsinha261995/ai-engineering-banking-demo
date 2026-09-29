# FDE AI Project

This repository contains a demo customer support system that combines:

- a terminal-based AI assistant in `app/`
- a FastAPI backend in `backend/`
- a simple retrieval-augmented generation (RAG) flow using knowledge stored in `knowledge/`

The project is meant to simulate a support agent that can answer policy questions and access customer account information through LLM tool calling and authenticated API access.

## What the project does

- Answers user questions with a chat-style CLI
- Uses OpenRouter-compatible LLM calls for responses
- Retrieves relevant knowledge from local policy text via embeddings and similarity search
- Calls customer service APIs for customer lookup and payment actions
- Validates JWT auth and role-based access for backend endpoints

## Repository structure

- `app/agent.py` - main conversational agent loop and tool-calling logic
- `app/llm.py` - OpenAI/OpenRouter client and request wrapper
- `app/config.py` - environment configuration for LLM settings
- `app/auth.py` - JWT helper used by the CLI to read user role from a token
- `app/customer_service.py` - HTTP client that calls the backend service
- `app/tool_registry.py` - tool registry used by the assistant
- `app/tool_executor.py` - executes LLM-selected tools and handles confirmation flow
- `app/chunker.py` - splits policy text into chunks
- `app/embeddings.py` - creates embeddings with the OpenRouter embedding model
- `app/vector_store.py` - builds and searches an in-memory vector store
- `app/knowledge.py` - keyword-based fallback knowledge lookup
- `app/test_rag.py` and `app/test_vector_store.py` - quick retrieval demos
- `knowledge/company_policies.txt` - source policy text used for RAG
- `backend/main.py` - FastAPI application
- `backend/auth.py` - login/register endpoints
- `backend/security.py` - password hashing, JWT creation/validation, role checks
- `backend/database.py` - SQLAlchemy database setup
- `backend/models.py` - database schema for customers, payments, and users
- `backend/init_db.py` - creates database tables and sample customer data
- `backend/schemas.py` - Pydantic request/response schemas
- `customers.db` - SQLite database file
- `requirements.txt` - project dependencies

## RAG flow

The knowledge layer is built around local policy text stored in `knowledge/company_policies.txt`.

The flow is:

1. `create_chunks()` splits the policy file into sections
2. `create_embedding()` generates vector embeddings
3. `build_vector_store()` stores chunk text and embeddings in memory
4. `search_vector_store()` finds the most relevant chunks by cosine similarity
5. The retrieved context is passed to the LLM as grounded support data

This lets the assistant answer policy-based questions using retrieved context instead of relying only on model memory.

## Backend API

The FastAPI app exposes these routes:

- `POST /auth/register` - create a user account
- `POST /auth/login` - log in and receive a JWT
- `GET /customers/{customer_id}` - fetch a customer record
- `GET /customers/{customer_id}/balance` - fetch the outstanding balance
- `POST /customers/{customer_id}/payments` - record a payment

Authentication is handled with bearer tokens and JWTs. Customer read endpoints require a valid bearer token. Payment creation is protected by a role check requiring the `admin` role.

## CLI usage

Start the backend:

```bash
uvicorn backend.main:app --reload
```

Then run the terminal assistant:

```bash
python app/main.py
```

The CLI prompts for a user access token before each request. This token is used in authenticated calls to the backend service.

## Environment variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL=your_model
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
JWT_SECRET=your_jwt_secret
```

The app expects these values to be present at runtime.

## Sample data

The project seeds sample customers at startup:

- 101 - Rahul Kumar
- 102 - Priya Sharma
- 103 - Amit Singh

These records are inserted by `backend/init_db.py` into the SQLite database.

## Notes

- The project is a prototype/demo and is not production-ready for real financial systems.
- The knowledge layer depends on local files and embeddings rather than a managed vector database.
- The customer assistant and backend are separate pieces, but they are designed to work together through authenticated HTTP requests.
