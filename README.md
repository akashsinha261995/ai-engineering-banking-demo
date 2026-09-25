# FDE AI Project

A small customer-support demo with an LLM-powered terminal assistant and a FastAPI service for customer and payment operations.

## Components

- `app/` - conversational assistant, LLM tool calling, and HTTP client for the service
- `backend/` - FastAPI endpoints, JWT authentication, and SQLite persistence

The API serves customer details and balances, and records validated payments. The assistant asks for confirmation before submitting a payment. Initial sample customers are created in the SQLite database at startup.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root with the required settings:

```env
OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL=your_model
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
JWT_SECRET=use-a-long-random-secret
```

Start the API from the project root:

```bash
uvicorn backend.main:app --reload
```

The API documentation is available at `http://127.0.0.1:8000/docs`. Register and log in through `/auth/register` and `/auth/login` to obtain a bearer token. The CLI asks for this token for each request; run it in another terminal:

```bash
python app/main.py
```

## API routes

- `POST /auth/register` and `POST /auth/login` - account registration and token issuance
- `GET /customers/{customer_id}` - customer details; requires a bearer token
- `GET /customers/{customer_id}/balance` - outstanding balance; requires a bearer token
- `POST /customers/{customer_id}/payments` - record a payment; requires the `admin` role

By default, new accounts have the `user` role. The current code does not provide an API route to grant the admin role.

## Notes

- The API stores data in `customers.db`; the CLI sends requests to `http://127.0.0.1:8000`.
- This is a prototype and is not intended for production financial use.
