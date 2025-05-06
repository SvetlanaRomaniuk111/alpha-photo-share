#TODO: add tag, tags to post, delete tag from post, get all tags for post, get all posts for user by tag 
# delete tag from PostTag table (interrelations between Post and Tag only ) 

from typing import List
from uuid import UUID
from fastapi import APIRouter, File, Form, HTTPException, Depends, UploadFile, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_limiter.depends import RateLimiter

from src.db.database import get_db
from src.models import User
from src.models.users import Role
from src.repository import tags as repositories_tags
from src.schemas.post import  PostResponseSchema
from src.services.roles import RoleAccessService


router = APIRouter(prefix='/tags', tags=['tags'])
all_roles_access = RoleAccessService([role for role in Role ])



@router.get('/', response_model=list[PostResponseSchema], dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def get_tags(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db)):

    tag = await repositories_tags.get_tag(limit, offset, db)
    return tag


@router.get('/{tag_id}', response_model=PostResponseSchema, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def get_tag_by_name(tag_id: UUID, db: AsyncSession = Depends(get_db)):


    tag = await repositories_tags.get_tag_by_name(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag not found")
    return tag


@router.get('/posts/{post_id}', response_model=list[PostResponseSchema], dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def get_tags_for_post(post_id: UUID, db: AsyncSession = Depends(get_db)):

    tags = await repositories_tags.get_tags_for_post(post_id, db)
    if tags is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tags not found for this post")
    return tags


@router.post('/', response_model=PostResponseSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def create_tag_for_post(title: str = Form(...), description: str = Form(...), image: UploadFile = File(...),tags: List[str] = Form(default=[]), db: AsyncSession = Depends(get_db),
                         user: User = Depends(all_roles_access)):
    
    tags = await repositories_tags.add_tag_for_post(title, description, "http://image_url.com",tags, user.id, db)
    return tags

@router.delete('/{tag_name}', response_model=PostResponseSchema, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def delete_tag_from_post(tag_name: UUID, db: AsyncSession = Depends(get_db)):

    tag = await repositories_tags.delete_tag_from_post(tag_name, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag not found")
    return tag
