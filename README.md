# AdmissionFlow

Multi-tenant student enquiry and admission management platform for coaching institutes.

## Monorepo

- `frontend/` — Next.js + React + TypeScript dashboard.
- `backend/` — FastAPI REST API and PostgreSQL persistence.
- `ai-service/` — FastAPI service for grounded admission FAQs.
- `backend/migrations/` — SQL schema.
- `docker-compose.yml` — local multi-service development environment.

## Run with Docker

Install Docker Desktop, then from the repository root:

```bash
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/docs
- AI service: http://localhost:8001/docs

For production, set strong secrets and integrate a real identity provider. The starter JWT verifier is for development only. Do not commit secrets.

## Run services individually

See `frontend/README.md`, `backend/README.md`, and `ai-service/README.md`.
