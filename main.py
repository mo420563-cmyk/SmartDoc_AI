from fastapi import FastAPI

from routes.ai import router as ai_router
from routes.documents import router as documents_router

app = FastAPI(
    title="SmartDoc AI",
    description="AI-powered Documents API with Gemini structured analysis and a read-only document agent.",
    version="1.0.0",
)


@app.get("/health", summary="Check service health")
def health():
    return {"status": "ok"}


app.include_router(documents_router)
app.include_router(ai_router)
