from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.master.router import router as master_router
from app.auth.router import router as auth_router
from app.profile.router import router as profile_router
from app.ideas.router import router as ideas_router
from app.ai.router import router as ai_router
from app.groups.router import router as groups_router
from app.proposals.router import router as proposals_router
from app.milestones.router import router as milestones_router
from app.submissions.router import router as submission_router
from app.dashboard.router import router as dashboard_router

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
app.include_router(ideas_router)
app.include_router(ai_router)
app.include_router(groups_router)
app.include_router(proposals_router)
app.include_router(milestones_router)
app.include_router(submission_router)
app.include_router(dashboard_router)

@app.get("/")
async def root():
    return {
        "message": "AI FYP Platform Backend is Running 🚀"
    }