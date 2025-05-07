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
from src.repository import comments as repository_comments

router = APIRouter(prefix="/comments", tags=["comments"])
router_admin_moderator_comments = APIRouter(prefix="/admin_moderator", tags=["admin or moderator"])
all_roles_access = RoleAccessService([role for role in Role])
admin_or_moderator_access = RoleAccessService([Role.admin, Role.moderator])
admin_or_moderator = [Role.admin, Role.moderator]


@router.post("/", response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: UUID,
    message: str,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db),
):
    post = await get_post(post_id, db)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return await repository_comments.create_comment(post_id, user.id, message, db)


@router.get("/{post_id}", response_model=list[CommentSchema], status_code=status.HTTP_200_OK)
async def get_comments(post_id: UUID, db: AsyncSession = Depends(get_db)):
    return await repository_comments.get_comments(post_id, db)


@router.put("/{comment_id}", response_model=CommentSchema, status_code=status.HTTP_200_OK)
async def update_comment(
    comment_id: UUID,
    message: str,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db),
):
    comment = await db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if comment.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can only edit your own comments"
        )
    return await repository_comments.update_comment(comment_id, message, db)


@router_admin_moderator_comments.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: UUID,
    user: User = Depends(admin_or_moderator_access),
    db: AsyncSession = Depends(get_db),
):
    comment = await db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if comment.user_id != user.id or user.role not in admin_or_moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can only edit your own comments"
        )
    await db.delete(comment)
    await db.commit()
