"""
This module defines API routes for managing post information.
Routes include CRUD operations on posts with rate limiting and user authentication.

"""

from uuid import UUID
from fastapi import APIRouter, File, Form, HTTPException, Depends, UploadFile, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_limiter.depends import RateLimiter

from src.db.database import get_db
from src.models import User
from src.models.users import Role
from src.repository import posts as repositories_posts
from src.schemas.post import  PostUpdateSchema, PostResponse
from src.services.auth import auth_service
from src.services.roles import RoleAccessService

router = APIRouter(prefix='/posts', tags=['posts'])
all_roles_access = RoleAccessService([role for role in Role ])


@router.get('/', response_model=list[PostResponse], dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def get_posts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db)):

    posts = await repositories_posts.get_posts(limit, offset, db)
    return posts


@router.get('/{post_id}', response_model=PostResponse, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def get_post(post_id: UUID, db: AsyncSession = Depends(get_db)):


    post = await repositories_posts.get_post(post_id, db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.post('/', response_model=PostResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def create_post(title: str = Form(...), description: str = Form(...), image: UploadFile = File(...), db: AsyncSession = Depends(get_db),
                         user: User = Depends(all_roles_access)):

    #TODO: add Svitlana`s service for image upload
    post = await repositories_posts.create_post(title, description, "http://image_url.com", user.id, db)
    return post


@router.put("/{post_id}", response_model=PostResponse, dependencies=[Depends(RateLimiter(times=10, seconds=20))])
async def update_post(body: PostUpdateSchema, post_id: UUID, user: User = Depends(all_roles_access), db: AsyncSession = Depends(get_db)):

    post = await repositories_posts.get_post(post_id, db)

    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this post")

    if body.title is None and body.description is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    post = await repositories_posts.update_post(body, post_id, db)
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
