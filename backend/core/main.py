from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.claims import router

app = FastAPI(title="Rumor vs. Reality API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "running"}
