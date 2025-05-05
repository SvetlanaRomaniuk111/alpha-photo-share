from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from src.db.database import get_db
from src.models.users import User
from src.models.posts import Post
from src.services.auth import auth_service
from src.schemas.user import UserProfileSchema
from src.services.roles import RoleAccessService, Role
from src.repository.posts import count_user_photos
from src.repository.user import update_user_profile, get_user_by_email, ban_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{email}", response_model=UserProfileSchema)
async def get_user_profile(email: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    photo_count = await count_user_photos(user.id, db)
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "created_at": user.created_at,
        "photo_count": photo_count,
    }


@router.get("/me", response_model=UserProfileSchema)
async def get_my_profile(user: User = Depends(auth_service.authenticate_user), db: AsyncSession = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="User is not authenticated")

    photo_count = await count_user_photos(user.id, db)

    return UserProfileSchema(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        created_at=user.created_at,
        photo_count=photo_count,
    )


@router.put("/me", response_model=UserProfileSchema)
async def update_my_profile(
    full_name: str,
    email: str,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db),
):
    return await update_user_profile(user, full_name, email, db)


@router.put("/{user_id}/ban")
async def ban_user_endpoint(
    user_id: UUID,
    admin: User = Depends(RoleAccessService([Role.admin])),
    db: AsyncSession = Depends(get_db),
):
    user = await ban_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User {user.email} has been banned"}
