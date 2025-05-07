"""
This module defines API routes for managing post information.
Routes include CRUD operations on posts with rate limiting and user authentication.

"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, File, Form, HTTPException, Depends, UploadFile, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_limiter.depends import RateLimiter

from src.db.database import get_db
from src.models import User
from src.models.users import Role
from src.repository import posts as repositories_posts
from src.schemas.post import PostResponseSchema
from src.services.roles import RoleAccessService
from src.services.image import cloudinary_service

router = APIRouter(prefix='/posts', tags=['posts'])
all_roles_access = RoleAccessService([role for role in Role])


@router.get('/', response_model=list[PostResponseSchema], dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def get_posts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db)):

    posts = await repositories_posts.get_posts(limit, offset, db)
    return posts


@router.get('/{post_id}', response_model=PostResponseSchema, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def get_post(post_id: UUID, db: AsyncSession = Depends(get_db)):


    post = await repositories_posts.get_post(post_id, db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.get('/tags/{tag_name}', response_model=list[PostResponseSchema], dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def get_posts_by_tag(tag_name: str, db: AsyncSession = Depends(get_db)):
    posts = await repositories_posts.get_posts_by_tag(tag_name, db)
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not found by this tag")
    return posts


@router.post('/', response_model=PostResponseSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def create_post(title: str = Form(...), description: str = Form(...), image: UploadFile = File(...),tags: Optional[List[str]] = Form(default=[]), db: AsyncSession = Depends(get_db),
                         user: User = Depends(all_roles_access)):
    tags = tags[0].split(",")
    if len(tags) > 5:
        raise HTTPException(status_code=400, detail="You can add up to 5 tags only.")
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is not an image")
    image_url = await cloudinary_service.upload(image, user.email)
    
    try:
        post = await repositories_posts.create_post(title, description, image_url, user.id, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create post: {e}")
    for tag_name in tags:
        cleaned_tag = tag_name.strip()
        if cleaned_tag:
            await repositories_posts.add_tag_for_post(post.id, cleaned_tag, db)

    return await repositories_posts.get_post(post.id, db)


@router.patch("/{post_id}", response_model=PostResponseSchema, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def update_post(title: Optional[str], description: Optional[str], post_id: UUID, user: User = Depends(all_roles_access), db: AsyncSession = Depends(get_db)):

    post = await repositories_posts.get_post(post_id, db)

    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this post")

    if title is None and description is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    post = await repositories_posts.update_post(title, description, post_id, db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def delete_post( post_id: UUID, user: User = Depends(all_roles_access), db: AsyncSession = Depends(get_db)):
    post = await repositories_posts.get_post(post_id, db)

    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this post")

    post = await repositories_posts.delete_post(post_id, db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
