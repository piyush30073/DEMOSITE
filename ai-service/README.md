# AI Service

FastAPI service for institute-approved FAQ answers.

1. `python -m venv .venv`
2. Activate environment and `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`; set a strong `SERVICE_API_KEY` and optional `OPENAI_API_KEY`.
4. `uvicorn app.main:app --reload --port 8001`

POST `/api/v1/faq/answer` with `X-Service-Key`. Keep this service private behind the backend in production. Pass only approved course facts; add rate limiting, tenant-scoped retrieval and data-retention controls before launch.
