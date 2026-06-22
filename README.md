# Satya Finder

Karnataka school rumor and circular fact-checker, built for the USAII Global AI Hackathon 2026.

Satya Finder lets parents, students, and teachers verify school-related claims — closures, fee hikes, safety alerts, policy changes — by pasting a message or uploading a screenshot. An AI research agent searches the live web, reads authoritative sources, and returns a sourced verdict with a confidence score, in seconds.

**Live demo:** https://satya-finder.vercel.app

## Architecture

Three independent services:

- **Frontend** — SvelteKit, deployed on Vercel. Accepts text input (English or Kannada) and optional image upload.
- **Backend** — FastAPI, deployed on Render. Orchestrates the pipeline, applies confidence thresholding, and persists claims to MongoDB.
- **Agent** — FastAPI + LangChain + Groq (Llama 3.3 70B). Runs a ReAct-style agentic loop with live web search and page-fetching tools.

## API Contract

The frontend POSTs to `POST /api/check` on the backend.

### Request

```json
{
  "claim": "string",
  "image": "base64 string or null"
}
```

### Response

```json
{
  "id": "uuid",
  "verdict": "True | False | Misleading | Unverified | null",
  "response": "Plain language explanation of what was found.",
  "confidence": 0.85,
  "flagged": false,
  "sources": ["https://source1.gov.in", "https://source2.gov.in"],
  "status": "completed | failed | processing | clarification_needed",
  "time": "2026-06-22T10:00:00Z"
}
```

### Error Response

```json
{
  "detail": "Error message here"
}
```

## Environment Variables

### Backend
| Variable | Description |
|---|---|
| `MONGO_URI` | MongoDB connection string |
| `AGENT_URL` | URL of the deployed agent service |

### Agent
| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key for Llama 3.3 70B |

### Frontend
| Variable | Description |
|---|---|
| `VITE_BACKEND_URL` | URL of the deployed backend service |

## Stack

python, javascript, svelte, sveltekit, fastapi, langchain, langgraph, groq api, llama 3.3 70b, duckduckgo search, mongodb, beautifulsoup, httpx, pydantic, uvicorn, vercel, render