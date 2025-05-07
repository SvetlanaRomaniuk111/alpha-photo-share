from sqlalchemy.ext.asyncio import AsyncSession
from src.models.posts import Comment
from uuid import UUID
from sqlalchemy.future import select


async def create_comment(post_id: UUID, user_id: UUID, message: str, db: AsyncSession):
    comment = Comment(post_id=post_id, user_id=user_id, message=message)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def get_comments(post_id: UUID, db: AsyncSession):
    stmt = (
        select(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at)
    )
    coments = await db.execute(stmt)
    return coments.scalars().all()


async def update_comment(comment_id: UUID, message: str, db: AsyncSession):
    comment = await db.get(Comment, comment_id)
    if comment:
        comment.message = message
        await db.commit()
        await db.refresh(comment)
    return comment


async def delete_comment(comment_id: UUID, db: AsyncSession):
    comment = await db.get(Comment, comment_id)
    if not comment:
        return False
    await db.delete(comment)
    await db.commit()
    return True
