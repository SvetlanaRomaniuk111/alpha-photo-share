from typing import List, Optional
from sqlalchemy import UUID, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Post, User
from src.models.posts import PostTag, Tag
from src.schemas.post import  PostUpdateSchema
from src.repository.exceptions import NotFoundError
from src.repository.tags import add_tag


# get all posts with pagination
async def get_posts(limit: int, offset: int, db: AsyncSession):

    stmt = select(Post).offset(offset).limit(limit).join(Post.tags)
    posts = await db.execute(stmt)
    return posts.scalars().all()


# get one post by id
async def get_post(post_id: UUID, db: AsyncSession):

    stmt = (
        select(Post)
        .where(Post.id == post_id)
        .join(PostTag, PostTag.post_id == Post.id)
        .join(Tag, Tag.id == PostTag.tag_id)
    )
    post = await db.execute(stmt)
    return post.scalar_one_or_none()
    


async def get_posts_by_tag(tag_name: str, db: AsyncSession):
    stmt = select(Post).join(Post.tags).where(Tag.name == tag_name)
    post = await db.execute(stmt)
    return post.scalars().all()


#TODO: add_tag_for_post
# args - post_id, name
# call get_post(post_id) and check 
# if post not exist -> err NotFoundError
# if post exists call add_tag(post_id, name) from tags repo 
# add (post_id, tag_id) to PostTag table
async def add_tag_for_post(post_id: UUID, name: str, db: AsyncSession):

    tag = await add_tag(name, db) 
    post_tag = PostTag(post_id=post_id, tag_id=tag.id)
    db.add(post_tag)
    await db.commit()
    await db.refresh(post_tag)
    return post_tag
    


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
