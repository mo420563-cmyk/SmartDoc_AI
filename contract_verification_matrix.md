# SmartDoc AI Contract Verification Matrix

| Method | Path | Case | Expected | Actual | Pass/Fail |
|---|---|---|---:|---:|---|
| GET | /health | service health | 200 | To verify locally | |
| GET | /documents | normal list | 200 | To verify locally | |
| POST | /documents | valid body | 201 | To verify locally | |
| POST | /documents | invalid body | 422 | To verify locally | |
| GET | /documents/999999 | missing document | 404 | To verify locally | |
| PUT | /documents/999999 | missing document | 404 | To verify locally | |
| DELETE | /documents/999999 | missing document | 404 | To verify locally | |
| POST | /documents/upload | unsupported type | 400 | To verify locally | |
| POST | /documents/{id}/analyze | existing document | 200 | To verify locally | |
| POST | /documents/{id}/analyze | missing document | 404 | To verify locally | |
| POST | /agent/ask | document question | 200 | To verify locally | |

A 200 response is considered a pass only when the response body and documented contract also match the expected behavior.
