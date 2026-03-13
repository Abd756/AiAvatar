from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import sessions

app = FastAPI(title="AiAvatar API")

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Add production URL if available in environment
import os
prod_url = os.getenv("FRONTEND_URL")
if prod_url:
    origins.append(prod_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router, prefix="/api/v1", tags=["Session"])

@app.get("/")
async def root():
    return {"message": "AiAvatar API is running"}

if __name__ == "__main__":
    import uvicorn
    # Use the full path from the project root
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
