from typing import List, Optional
from sqlalchemy import UUID, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.models import Post, User
from src.models.posts import PostTag, Tag
from src.repository.tags import add_tag


# get all posts with pagination
async def get_posts(limit: int, offset: int, db: AsyncSession):
    result = await db.execute(
        select(Post)
        .options(
            joinedload(Post.tags).joinedload(PostTag.tag)
        )
        .offset(offset).limit(limit)
    )
    return result.scalars().unique().all()


# get one post by id
async def get_post(post_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(Post)
        .options(
            joinedload(Post.tags).joinedload(PostTag.tag)
        )
        .where(Post.id == post_id)
    )
    post = result.unique().scalar_one_or_none()
    return post
    


async def get_posts_by_tag(tag_name: str, db: AsyncSession):
    result = await db.execute(
        select(Post)
        .join(Post.tags)
        .join(PostTag.tag)
        .options(
            selectinload(Post.tags).selectinload(PostTag.tag)  
        )
        .where(Tag.name == tag_name)
    )
    return result.unique().scalars().all()



async def add_tag_for_post(post_id: UUID, name: str, db: AsyncSession):

    tag_id = await add_tag(name, db) 
    post_tag = PostTag(post_id=post_id, tag_id=tag_id)
    db.add(post_tag)
    await db.commit()
    await db.refresh(post_tag)

    


#create post
async def create_post(title: str, description: str, image_url: str, user_id: UUID, db: AsyncSession):
    
    post = Post(
        title=title,
        description=description,
        image_url=image_url,
        user_id=user_id,
    )

    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post 

   

# update post
async def update_post(title, description, post_id: UUID, db: AsyncSession):

    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if post:
        if title is not None:
            post.title = title
        if description is not None:
            post.description = description
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
    stmt = select(func.count()).select_from(Post).filter(Post.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one()