from fastapi import APIRouter, HTTPException, Depends, Request, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.repository import user as repositories_users
from src.schemas.user import UserCreationSchema, TokenSchema, UserResponseSchema
from src.core import log
from src.services.auth import auth_service

auth_router = APIRouter(prefix='/auth', tags=['auth'])
get_refresh_token = HTTPBearer()


@auth_router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(body: UserCreationSchema, request: Request, db: AsyncSession = Depends(get_db)):
    """
    Sign up a new user.

    This endpoint allows a new user to create an account. If the email already exists, a conflict is raised.
    The password is hashed before being saved. A confirmation email is sent after the user is created.

    Args:
        body (UserCreationSchema): The user creation data, including email and password.
        request (Request): The HTTP request object to retrieve base URL for email.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the user already exists (409 Conflict).

    Returns:
        UserResponseSchema: The newly created user details.
    """
    exist_user = await repositories_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repositories_users.create_user(body, db)
    log.info(f"User {new_user.email} created")
    return new_user

@auth_router.post("/login",  response_model=TokenSchema)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Log in a user and return JWT tokens.

    This endpoint allows a user to log in by providing their credentials. If the credentials are valid,
    an access token and a refresh token are generated and returned.

    Args:
        body (OAuth2PasswordRequestForm): The login credentials (username and password).
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the user credentials are invalid or the email is not verified (401 Unauthorized).

    Returns:
        dict: A dictionary containing the access token, refresh token, and token type.
    """
    user = await repositories_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repositories_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@auth_router.get('/refresh_token',  response_model=TokenSchema)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
                        db: AsyncSession = Depends(get_db)):
    """
    Refresh the access token using the refresh token.

    This endpoint allows the user to refresh their access token by providing a valid refresh token.
    A new access token and refresh token are returned.

    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP credentials containing the refresh token.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the refresh token is invalid or does not match the one stored for the user (401 Unauthorized).

    Returns:
        dict: A dictionary containing the new access token, refresh token, and token type.
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repositories_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repositories_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repositories_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

