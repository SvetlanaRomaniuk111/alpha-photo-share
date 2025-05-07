#TODO: add tag, tags to post, delete tag from post, get all tags for post, get all posts for user by tag 
# delete tag from PostTag table (interrelations between Post and Tag only ) 

from typing import List
from uuid import UUID
from fastapi import APIRouter, File, Form, HTTPException, Depends, UploadFile, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.exc import IntegrityError

from src.db.database import get_db
from src.models import User
from src.models.users import Role
from src.repository import tags as repositories_tags
from src.repository import posts as repositories_posts
from src.schemas.post import  PostResponseSchema, TagResponseSchema
from src.services.roles import RoleAccessService


router = APIRouter(prefix='/tags', tags=['tags'])
all_roles_access = RoleAccessService([role for role in Role ])



@router.get('/', response_model=list[TagResponseSchema], status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def get_tags_for_post(post_id: UUID, db: AsyncSession = Depends(get_db)):

    tags = await repositories_tags.get_tags_for_post(post_id, db)
    if tags is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tags not found for this post")
    return tags

@router.post('/', response_model=PostResponseSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def add_tag_for_post(post_id: UUID, tag_name: str, db: AsyncSession = Depends(get_db),
                         user: User = Depends(all_roles_access)):
    try:
        await repositories_posts.add_tag_for_post(post_id, tag_name, db)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Cannot add more than 5 tags to a post.")
    return await repositories_posts.get_post(post_id, db)

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def delete_tag_from_post(tag_name: str, post_id: UUID, db: AsyncSession = Depends(get_db)):
    tag = await repositories_tags.get_tag_by_name(tag_name, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag not found")
    post = await repositories_posts.get_post(post_id, db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    await repositories_tags.delete_tag_from_post(tag, post, db)
