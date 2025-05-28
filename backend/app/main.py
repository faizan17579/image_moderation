from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, moderate

app = FastAPI(title="Image Moderation API")

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(moderate.router, prefix="/moderate", tags=["moderate"])

@app.get("/")
async def root():
    return {"message": "Image Moderation API"}