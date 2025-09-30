from http.client import HTTPException

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from user.schemas import UserReadSchema, UserCreateSchema, AccessTokenSchema, UserUpdateSchema
from .jwt_repository import CredentialsRepository
from .models import User
from .repository import Repository

router = APIRouter(tags=["users"], prefix="/users")
get_token = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.post("/register")
async def register(user: UserCreateSchema, session: AsyncSession = Depends(get_async_session),
                   repository: Repository = Depends()) -> None:
    user = await repository.create_user(user, session)

@router.post("/login")
async def login(session: AsyncSession = Depends(get_async_session),
                credentials: OAuth2PasswordRequestForm = Depends(),
                repository_user: Repository = Depends(),
                repository: CredentialsRepository = Depends()) -> AccessTokenSchema:
    user = await repository_user.get_user(credentials.username, credentials.password, session)
    token = repository.make_token(user.nickname)
    return AccessTokenSchema(
        access_token=token,
        token_type="Bearer"
    )

@router.get("/data")
async def get_data(token: str = Depends(get_token), repository: CredentialsRepository = Depends(),
                   repository_user: Repository = Depends(),
                   session: AsyncSession = Depends(get_async_session)) -> str:
    if repository.is_valid_token(token):
        username = repository.decode_token(token)
        return await repository_user.get_data_by_username(username, session)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: int, token: str = Depends(get_token), repository_user: Repository = Depends(),
                            repository: CredentialsRepository = Depends(),
                            session: AsyncSession = Depends(get_async_session)) -> None:
    if repository.is_valid_token(token):
        username = repository.decode_token(token)
        user = await repository_user.delete_user_by_id(user_id, session, username)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )
    
@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user_by_id(user_id: int, user: UserUpdateSchema, token: str = Depends(get_token), session = Depends(get_async_session),
                            repository_user: Repository = Depends(),
                            repository: CredentialsRepository = Depends()) -> UserReadSchema:
    if repository.is_valid_token(token):
        username = repository.decode_token(token)
        return await repository_user.update_user_by_id(user_id, session, user, username )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )

@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(repository: Repository = Depends(),
                    session = Depends(get_async_session)) -> list[UserReadSchema]:
    return await repository.get_users(session)

