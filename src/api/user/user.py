from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import APIRouter, HTTPException, Depends, status
from uuid import UUID
from pydantic import EmailStr

from src.db.database import get_db
from src.models.users import User, Gender
from src.models.posts import Post
from src.services.auth import auth_service
from src.schemas.user import UserProfileSchema, UpdateUserProfileSchema, UserMeSchema
from src.services.roles import RoleAccessService, Role
from src.repository.posts import count_user_photos
from src.repository.user import update_user_profile, get_user_by_email, ban_user, get_user_by_id

router = APIRouter(prefix="/users", tags=["users"])
router_admin_moderator_work_with_user = APIRouter(prefix="/users", tags=["admin"])

@router.get("/me", response_model=UserMeSchema, status_code=status.HTTP_200_OK)
async def get_profile(
    user: User = Depends(auth_service.authenticate_user),
):
    return user

@router.get("/{email}", response_model=UserProfileSchema, status_code=status.HTTP_200_OK)
async def get_user_profile(email: EmailStr, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    photo_count = await count_user_photos(user.id, db)
    
    return UserProfileSchema(
        email=user.email,
        full_name=user.full_name,
        gender=user.gender,
        age=user.age,
        photo_count=photo_count,
    )




@router.patch("/me", response_model=UserMeSchema, status_code=status.HTTP_200_OK)
async def update_profile(
    full_name: Optional[str] = None,
    age: Optional[int] = None,
    gender: Optional[Gender] = None,
    password: Optional[str] = None,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db),
):
    if not any([full_name, age, gender, password]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one field must be provided.")
    return await update_user_profile(user, full_name, age, gender, password, db)


@router.patch("/ban/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleAccessService([Role.admin]))])
async def ban_user_endpoint(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    user: User = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        return {"message": f"User {user.email} is already banned"}
    user = await ban_user(user, db)
    return {"message": f"User {user.email} has been banned"}
