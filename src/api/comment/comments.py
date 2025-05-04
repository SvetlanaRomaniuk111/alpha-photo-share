from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.database import get_db
from src.models import User, Comment
from src.models.users import Role
from src.schemas.comments import CommentSchema
from src.services.auth import auth_service
from src.services.roles import RoleAccessService

router = APIRouter(prefix='/comments', tags=['comments'])
all_roles_access = RoleAccessService([role for role in Role])

@router.post("/", response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: UUID, message: str,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db)
):
    if not message:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty")
    
    comment = Comment(post_id=post_id, user_id=user.id, message=message)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


@router.get("/{post_id}", response_model=list[CommentSchema])
async def get_comments(post_id: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.put("/{comment_id}", response_model=CommentSchema)
async def edit_comment(
    comment_id: UUID, message: str,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db)
):
    comment = await db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    if comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="Редагувати можна тільки свої коментарі")

    comment.message = message
    await db.commit()
    await db.refresh(comment)
    return comment

@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: UUID,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db)
):
    comment = await db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    if user.role not in [Role.admin, Role.moderator]:
        raise HTTPException(status_code=403, detail="Видаляти можуть тільки адміністратори")

    await db.delete(comment)
    await db.commit()
    return {"message": "Коментар видалено"}