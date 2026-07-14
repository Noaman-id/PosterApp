from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api.v1.auth import auth_router
from app.api.v1.user import users_router
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="UserPost",
              description="UserPost help people authenticate and post there content")

app.include_router(users_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)