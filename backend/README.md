# Backend API

FastAPI + PostgreSQL service.

1. `python -m venv .venv`
2. Activate it and `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`; configure DATABASE_URL and a long random JWT_SECRET.
4. Apply `migrations/001_init.sql` to PostgreSQL.
5. Run `uvicorn app.main:app --reload --port 8000`.
6. API docs: http://localhost:8000/docs

Protected endpoints require a signed HS256 JWT with `sub` and `org` claims. This is a development integration boundary. Before production, replace it with Supabase Auth/JWKS validation and verify organization membership and roles on every request. Never use the sample secret in production.
