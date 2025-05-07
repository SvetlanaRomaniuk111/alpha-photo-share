from typing import List
from sqlalchemy import UUID, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_

from src.models import Tag, Post
from src.models.posts import PostTag



async def get_tag_by_name(tag_name: str, db: AsyncSession):
    stmt = select(Tag).where(Tag.name == tag_name)
    tag = await db.execute(stmt)
    return tag.scalar_one_or_none()


async def get_tags_for_post(post_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(Tag)
        .join(PostTag)
        .where(PostTag.post_id == post_id)
    )
    tags = result.scalars().all()
    return tags


async def add_tag(name : str, db: AsyncSession):

    stmt = select(Tag).where(Tag.name == name)
    tag = await db.execute(stmt)
    tag = tag.scalar_one_or_none()
    if tag is None:
        tag = Tag(name=name)
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
    
    return tag.id

async def delete_tag_from_post(tag: Tag, post: Post, db: AsyncSession):
    stmt = select(PostTag).where(and_(PostTag.tag_id == tag.id, PostTag.post_id == post.id))
    tag = await db.execute(stmt)
    tag = tag.scalar_one_or_none()
    if tag:
        await db.delete(tag)
        await db.commit()

