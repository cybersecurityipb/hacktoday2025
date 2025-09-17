from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import api
from src.utils import lifespan


app = FastAPI(lifespan=lifespan)

app.include_router(api, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
