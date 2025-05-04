from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.models.posts import Comment
from src.models.users import Role
from src.schemas.comments import CommentSchema
from src.models.users import User
from src.services.auth import auth_service
from src.services.roles import RoleAccessService
from src.repository.posts import get_post
from src.repository.comments import (
    create_comment as create_comment_in_db,
    get_comments as get_comments_from_db,
    update_comment as update_comment_in_db,
)

router = APIRouter(prefix="/comments", tags=["comments"])
all_roles_access = RoleAccessService([role for role in Role])
admin_or_moderator_access = RoleAccessService([Role.admin, Role.moderator])


@router.post("/", response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: UUID,
    message: str,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db),
):
    if not message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty"
        )
    post = await get_post(post_id, db)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return await create_comment_in_db(post_id, user.id, message, db)


@router.get("/{post_id}", response_model=list[CommentSchema])
async def get_comments(post_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_comments_from_db(post_id, db)


@router.put("/{comment_id}", response_model=CommentSchema)
async def update_comment(
    comment_id: UUID,
    message: str,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db),
):
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    comment = await db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="You can only edit your own comments"
        )
    return await update_comment_in_db(comment_id, message, db)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: UUID,
    user: User = Depends(admin_or_moderator_access),
    db: AsyncSession = Depends(get_db),
):
    comment = await db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    await db.delete(comment)
    await db.commit()
    return {"message": "Comment deleted"}
