# Satya Finder

Karnataka Education Circular and News Fact Checker — USAII Global AI Hackathon 2026.

## Backend Contract

The frontend POSTs to `POST /check` on the backend.

### Request

```json
{
  "text": "string or null",
  "image": "base64 string or null"
}
```

At least one of `text` or `image` must be non-null.

### Response

```json
{
  "verdict": "True | False | Misleading | Unverified",
  "confidence": 85,
  "explanation": "Plain language explanation of what was found.",
  "sources": ["https://source1.gov.in", "https://source2.gov.in"]
}
```

### Error Response

```json
{
  "detail": "Error message here"
}
```

## Deploy

Push to GitHub and connect to Vercel. Set `VITE_BACKEND_URL` in Vercel environment variables to the Render backend URL.