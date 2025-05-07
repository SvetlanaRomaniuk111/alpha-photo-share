from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.models.users import Role, User, Gender
from src.schemas.user import UserCreationSchema
from src.core import config, log
from src.services.auth import auth_service



async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a user by their email address.

    This function queries the database to find a user by their email address.

    Args:
        email (str): The email address of the user.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User | None: The user object if found, or None if the user does not exist.
    """
    stmt = select(User).filter(User.email == email)
    user = await db.execute(stmt)
    user = user.unique().scalar_one_or_none()
    return user


async def create_user(body: UserCreationSchema, db: AsyncSession = Depends(get_db)):
    """
    Create a new user in the database.

    This function creates a new user by extracting the data from the provided
    UserCreationSchema and saving it to the database.

    Args:
        body (UserCreationSchema): The user creation data, including email and password.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User: The newly created user object.
    """
    user = User(**body.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    Update the user's refresh token in the database.

    This function updates the user's refresh token with the new value provided.

    Args:
        user (User): The user object whose token is being updated.
        token (str | None): The new refresh token value. If None, the token will be cleared.
        db (AsyncSession): The database session to commit changes.
    """
    user.refresh_token = token
    await db.commit()


async def get_all_users_from_db(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User))
    users = list(result.scalars().all())  # Явна конвертація
    return users


async def delete_user(email, db: AsyncSession) -> List[User]:
    stmt = delete(User).where(User.email == email)
    await db.execute(stmt)
    await db.commit()
    return await get_all_users_from_db(db)  # Повертаємо всіх після видалення


async def update_user(email: str, update_data: dict, db: AsyncSession) -> User:
    user = await get_user_by_email(email, db)
    if not user:
        raise ValueError(f"User with email {email} not found.")
    for key, value in update_data.items():
        if value is not None:
            setattr(user, key, value)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_admin(db: AsyncSession) -> User:
    # Check if admin already exists
    admin_user = await get_user_by_email(config.admin_config.ADMIN_EMAIL, db)

    if admin_user:
        log.info(f"Admin user {config.admin_config.ADMIN_EMAIL} already exists.")
        return admin_user  # Return the existing admin user
    admin_user = User(
        full_name=config.admin_config.ADMIN_FULLNAME,
        email=config.admin_config.ADMIN_EMAIL,
        password=auth_service.get_password_hash(config.admin_config.ADMIN_PASSWORD),
        age=config.admin_config.ADMIN_AGE,
        gender=config.admin_config.ADMIN_GENDER,
        role=Role.admin,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(admin_user)
    await db.commit()
    await db.refresh(admin_user)
    return admin_user  # Ensure the newly created admin user is returned


async def get_user_by_id(user_id: UUID, db: AsyncSession):
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def update_user_profile(user: User,
        full_name: Optional[str],
        age: Optional[int],
        gender: Optional[Gender],
        password: Optional[str],
        db: AsyncSession
    ):

    if full_name is not None:
        user.full_name = full_name
    if age is not None:
        user.age = age
    if gender is not None:
        user.gender = gender
    if password is not None:
        user.password = auth_service.get_password_hash(password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def ban_user(user: User, db: AsyncSession):
    if user:
        user.is_active = False
        await db.commit()
        await db.refresh(user)
    return user
