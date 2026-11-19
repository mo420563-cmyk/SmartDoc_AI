@echo off
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/documents
curl -i -X POST http://127.0.0.1:8000/documents ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Curl Doc\",\"content\":\"FastAPI with Gemini\",\"priority\":2,\"description\":\"Capstone\"}"
curl -i http://127.0.0.1:8000/documents/1
curl -i -X POST http://127.0.0.1:8000/documents/1/analyze
curl -i -X POST http://127.0.0.1:8000/agent/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"List the available documents\"}"
curl -i -X POST http://127.0.0.1:8000/documents ^
  -H "Content-Type: application/json" ^
  -d "{}"
curl -i http://127.0.0.1:8000/documents/999999
curl -i -X POST http://127.0.0.1:8000/documents/999999/analyze
