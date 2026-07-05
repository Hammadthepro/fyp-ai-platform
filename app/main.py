from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.master.router import router as master_router
from app.auth.router import router as auth_router
from app.profile.router import router as profile_router

app = FastAPI(
    title="AI FYP Platform API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(master_router)


@app.get("/")
async def root():
    return {
        "message": "AI FYP Platform Backend is Running 🚀"
    }