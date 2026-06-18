# This is the main script that exposes the backend
# it uses FastAPI and the CORSMiddleWare as a middleware and a router to route all relevant calls to thier respectiove function
# Importing Necessary Librarieas
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
router = None # current defining router as None since it is not built, after building use, from routes.claims import router, for the router

app = FastAPI(title="USAII Project App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router=router)

# Verify App is running
@app.get("/health")
async def health() -> None:
    return {"status": "running"}