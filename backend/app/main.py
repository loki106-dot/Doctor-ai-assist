# import sys
# import os

# # 🔑 Add project root to PYTHONPATH (Windows + uvicorn fix)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# if BASE_DIR not in sys.path:
#     sys.path.insert(0, BASE_DIR)

# from fastapi import FastAPI
# from app.api.chat import router as chat_router


# app = FastAPI(
#     title="Smart Doctor AI Assistant",
#     version="1.0.0"
# )

# app.include_router(chat_router)

# @app.get("/health")
# def health_check():
#     return {"status": "ok"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router

app = FastAPI()

# -------------------------------
# CORS CONFIG (IMPORTANT)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Routes
# -------------------------------
app.include_router(chat_router)

@app.get("/")
def root():
    return {"status": "Doctor AI Backend Running"}
