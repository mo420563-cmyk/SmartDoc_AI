import json
import logging

from google import genai
from google.genai import types
from sqlalchemy import or_, cast, String
from sqlalchemy.orm import Session

from database import engine
from models import Document
from settings import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)
MAX_STEPS = 5


def list_documents_tool():
    with Session(engine) as db:
        rows = db.query(Document).all()
        return [{"id": d.id, "title": d.title, "priority": d.priority} for d in rows]


def get_document_tool(document_id: int):
    if document_id <= 0:
        raise ValueError("document_id must be greater than 0")
    with Session(engine) as db:
        document = db.get(Document, document_id)
        if document is None:
            return None
        return {
            "id": document.id,
            "title": document.title,
            "content": document.content,
            "priority": document.priority,
            "description": document.description,
            "ai_summary": document.ai_summary,
        }


def search_documents_tool(query: str):
    if not query or len(query) > 200:
        raise ValueError("query must be between 1 and 200 characters")
    with Session(engine) as db:
        pattern = f"%{query}%"
        rows = db.query(Document).filter(
            or_(Document.title.ilike(pattern), cast(Document.id, String).ilike(pattern))
        ).all()
        return [{"id": d.id, "title": d.title, "priority": d.priority} for d in rows]


TOOLS = {
    "list_documents": list_documents_tool,
    "get_document": get_document_tool,
    "search_documents": search_documents_tool,
}

TOOL_DECLARATIONS = [
    types.FunctionDeclaration(
        name="list_documents",
        description="List available documents with id, title, and priority.",
        parameters_json_schema={"type": "object", "properties": {}},
    ),
    types.FunctionDeclaration(
        name="get_document",
        description="Get the selected document fields. document_id must be greater than 0.",
        parameters_json_schema={
            "type": "object",
            "properties": {"document_id": {"type": "integer"}},
            "required": ["document_id"],
        },
    ),
    types.FunctionDeclaration(
        name="search_documents",
        description="Search documents by title or id.",
        parameters_json_schema={
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    ),
]


def ask_agent(message: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini API key is not configured")

    client = genai.Client(api_key=GEMINI_API_KEY)
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=(
                "You are a read-only document assistant. Answer only from information returned by your tools. "
                "Never invent document facts. You may use only the whitelisted tools. "
                "You cannot create, update, or delete documents.\n\nUser question: " + message
            ))],
        )
    ]
    config = types.GenerateContentConfig(tools=[types.Tool(function_declarations=TOOL_DECLARATIONS)])

    for step in range(MAX_STEPS):
        response = client.models.generate_content(model=GEMINI_MODEL, contents=contents, config=config)
        function_calls = response.function_calls or []
        if not function_calls:
            answer = response.text
            if not answer:
                raise RuntimeError("Agent returned an empty answer")
            return answer

        contents.append(response.candidates[0].content)
        tool_parts = []
        for call in function_calls:
            name = call.name
            args = call.args or {}
            if name not in TOOLS:
                logger.warning("tool=%s success=false", name)
                tool_parts.append(types.Part.from_function_response(
                    name=name,
                    response={"error": "Tool is not allowed"},
                ))
                continue
            try:
                if name == "get_document":
                    document_id = int(args.get("document_id"))
                    result = TOOLS[name](document_id)
                elif name == "search_documents":
                    result = TOOLS[name](str(args.get("query", "")))
                else:
                    result = TOOLS[name]()
                logger.info("tool=%s success=true", name)
                observation = {"result": result}
            except Exception:
                logger.exception("tool=%s success=false", name)
                observation = {"error": "Tool execution failed"}
            tool_parts.append(types.Part.from_function_response(name=name, response=observation))

        contents.append(types.Content(role="tool", parts=tool_parts))

    raise RuntimeError("Agent reached the maximum number of steps")
