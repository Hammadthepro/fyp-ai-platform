from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.enums.roles import UserRole


def require_role(role: UserRole):

    async def checker(
        current_user=Depends(get_current_user),
    ):

        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied.",
            )

        return current_user

    return checker