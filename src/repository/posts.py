from sqlalchemy import UUID, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Post, User
from src.schemas.post import  PostUpdateSchema


# get all posts with pagination
async def get_posts(limit: int, offset: int, db: AsyncSession):

    stmt = select(Post).offset(offset).limit(limit)
    posts = await db.execute(stmt)
    return posts.scalars().all()


# get one post by id
async def get_post(post_id: UUID, db: AsyncSession):

    stmt = select(Post).where(Post.id == post_id)
    post = await db.execute(stmt)
    return post.scalar_one_or_none()

#create post
async def create_post(title: str, description: str, image_url: str, user_id: UUID, db: AsyncSession):

    post = Post(
        title=title,
        description=description,
        image_url=image_url,
        user_id=user_id
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

# update post
async def update_post(body: PostUpdateSchema, post_id: UUID, db: AsyncSession):

    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if post:
        if body.title is not None:
            post.title = body.title
        if body.description is not None:
            post.description = body.description
        await db.commit()
        await db.refresh(post)
    return post

# delete post
async def delete_post(post_id: UUID, db: AsyncSession):

    stmt = select(Post).where(Post.id == post_id)
    post = await db.execute(stmt)
    post = post.scalar_one_or_none()
    if post:
        await db.delete(post)
        await db.commit()
    return post

async def count_user_photos(user_id: UUID, db: AsyncSession) -> int:
    stmt = select(Post).filter(Post.user_id == user_id)
    result = await db.execute(stmt)
    return len(result.scalars().all())