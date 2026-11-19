# AI-Assisted Development Review

## Scoped Change

Added `POST /documents/{document_id}/analyze` in `routes/ai.py` using the existing `Document` model and `with Session(engine) as db` pattern.

## Prompt Used

```text
In routes/ai.py, add POST /documents/{document_id}/analyze.
Reuse the existing Document model and Session(engine) pattern.
Return 404 when the document is missing.
Do not change the existing CRUD routes.
Keep the response compatible with AIAnalysisResponse.
```

## Manual Review

I reviewed the generated change before keeping it. I verified that the route returns 404 for a missing document, reads the document from SQLite with the existing Session(engine) pattern, and does not expose the Gemini API key. I also verified that the summary is saved to `ai_summary` after successful analysis and that Gemini failures are converted into a controlled HTTP error.
