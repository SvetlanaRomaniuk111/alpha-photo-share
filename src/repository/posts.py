from sqlalchemy import UUID, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Post, User
from src.schemas.post import PostCreationSchema, PostUpdateSchema


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
async def create_post(body: PostCreationSchema, user: User, db: AsyncSession):

    post = Post(**{**body.model_dump(), 'user_id': user.id})
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

# update post
async def update_post(body: PostUpdateSchema, post_id: UUID , user : User, db: AsyncSession):

    stmt = select(Post).where(Post.id == post_id, Post.user_id == user.id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if post:
        post.title = body.title
        post.description = body.description
        post.image_url = body.image_url
        await db.commit()
        await db.refresh(post)
    return post

# delete post
async def delete_post(post_id: UUID, user: User, db: AsyncSession):

    stmt = select(Post).where(Post.id == post_id, Post.user_id == user.id)
    post = await db.execute(stmt)
    post = post.scalar_one_or_none()
    if post:
        await db.delete(post)
        await db.commit()
    return post
