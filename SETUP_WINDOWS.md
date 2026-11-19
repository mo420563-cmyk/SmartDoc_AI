# SmartDoc AI Lab 6 - Windows Setup

1. Open this folder in VS Code.
2. Open Terminal.
3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Create `.env` by copying `.env.example`, then put your Gemini API key in `GEMINI_API_KEY`. Do not share the key.

5. Run the database migration:

```powershell
python -m alembic upgrade head
```

6. Start the API:

```powershell
uvicorn main:app --reload
```

7. Open Swagger:
`http://127.0.0.1:8000/docs`

The Alembic migrations are safe for both a fresh empty database and an existing Lecture 4/5 `documents.db`.
