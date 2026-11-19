# SmartDoc AI

ITI Cross-Course Capstone Project.

SmartDoc AI is a FastAPI document backend that stores documents in SQLite, analyzes document content with Gemini, and provides a controlled read-only document agent.

## Project Structure

```text
smartdoc_ai/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── settings.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── contract_verification_matrix.md
├── postman_collection.json
├── routes/
│   ├── __init__.py
│   ├── documents.py
│   └── ai.py
├── services/
│   ├── __init__.py
│   ├── gemini_service.py
│   └── agent_service.py
├── alembic.ini
└── alembic/
    ├── env.py
    └── versions/
        ├── 0001_add_description.py
        └── 0002_add_ai_summary.py
```

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Keep the existing `documents.db` from the Lecture 4/5 project in the project folder.

## Configure

Create `.env` from `.env.example` and set your Gemini API key.

Never commit `.env` or a real API key.

## Migrate

```bash
python -m alembic current
python -m alembic upgrade head
python -m alembic current
```

The migration adds `ai_summary` without deleting existing documents.

## Run

```bash
uvicorn main:app --reload
```

Open:

- `/docs`
- `/redoc`
- `/openapi.json`

## API Endpoints

- `GET /health`
- `GET /documents`
- `POST /documents`
- `GET /documents/{id}`
- `PUT /documents/{id}`
- `DELETE /documents/{id}`
- `POST /documents/upload`
- `POST /documents/{id}/analyze`
- `POST /agent/ask`

## Gemini Analysis

Example request:

```json
{
  "title": "API Notes",
  "content": "FastAPI is a Python framework for building APIs.",
  "priority": 2,
  "description": "FastAPI notes"
}
```

Then call:

```text
POST /documents/{id}/analyze
```

The analysis returns structured JSON with `summary`, `key_points`, `category`, and `suggested_priority`, and only the returned summary is saved to `ai_summary`.

## Read-only Agent

Example:

```json
{
  "message": "Find the API notes and tell me their key idea"
}
```

The agent can use only:

- `list_documents`
- `get_document`
- `search_documents`

The Python application validates and executes tool calls. `MAX_STEPS = 5` prevents endless loops.

## Upload

`POST /documents/upload` accepts `text/plain` UTF-8 files and stores the decoded text in `Document.content`.

## Testing

Use Swagger, Windows CMD curl, and Postman.

Postman requests are included in `postman_collection.json`.

The contract matrix is included in `contract_verification_matrix.md`.

## AI-Assisted Development Review

See `ai_assisted_review.md` for the scoped AI-coding change, prompt, and manual review note.
