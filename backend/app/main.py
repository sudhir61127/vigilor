from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import get_database
from app.api.routes import router

@asynccontextmanager
async def lifespan(_: FastAPI):
    get_database()
    yield

app = FastAPI(title="VIGIL-OR", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Include API routes
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "healthy", "service": "vigil-or"}
