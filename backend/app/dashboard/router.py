from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.dashboard.service import DashboardService
from app.models.user import User

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# ==========================================================
# STUDENT DASHBOARD
# ==========================================================

@router.get("/student")
async def student_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = DashboardService(db)

    dashboard = await service.student_dashboard(
        current_user
    )

    if dashboard is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found.",
        )

    student = dashboard["student"]
    proposal = dashboard["proposal"]

    return {
        "student_name": student.user.full_name,
        "department": student.department,
        "semester": student.semester,
        "group_name": (
            dashboard["group"].name
            if dashboard["group"]
            else None
        ),
        "progress": dashboard["progress"],
        "completed_milestones": dashboard["completed"],
        "total_milestones": dashboard["total"],
        "proposal": (
            {
                "id": proposal.id,
                "title": proposal.title,
                "status": proposal.status,
                "professor": (
                    proposal.professor.user.full_name
                    if proposal.professor
                    else None
                ),
            }
            if proposal
            else None
        ),
        "milestones": [
            {
                "id": m.id,
                "title": m.title,
                "due_date": m.due_date,
                "status": m.status,
            }
            for m in dashboard["milestones"]
        ],
        "notifications": [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "type": n.type,
                "is_read": n.is_read,
                "created_at": n.created_at,
            }
            for n in dashboard["notifications"]
        ],
    }


# ==========================================================
# PROFESSOR DASHBOARD
# ==========================================================

@router.get("/professor")
async def professor_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = DashboardService(db)

    dashboard = await service.professor_dashboard(
        current_user
    )

    if dashboard is None:
        raise HTTPException(
            status_code=404,
            detail="Professor not found.",
        )

    professor = dashboard["professor"]

    return {
        "professor_name": professor.user.full_name,
        "total_groups": dashboard["total_groups"],
        "total_proposals": dashboard["total_proposals"],
        "pending_proposals": dashboard["pending"],
        "approved_proposals": dashboard["approved"],
        "rejected_proposals": dashboard["rejected"],
        "proposals": [
            {
                "id": p.id,
                "title": p.title,
                "group_name": (
                    p.group.name
                    if p.group
                    else None
                ),
                "status": p.status,
            }
            for p in dashboard["proposals"]
        ],
    }


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

@router.get("/admin")
async def admin_dashboard(
    db: AsyncSession = Depends(get_db),
):

    service = DashboardService(db)

    return await service.admin_dashboard()


# ==========================================================
# ANALYTICS
# ==========================================================

@router.get("/analytics")
async def dashboard_analytics(
    db: AsyncSession = Depends(get_db),
):

    service = DashboardService(db)

    return await service.analytics()