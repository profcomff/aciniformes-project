from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status
from fastapi.requests import Request
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from aciniformes_backend.serivce import AuthServiceInterface, auth_service
import aciniformes_backend.serivce.exceptions as exc
from aciniformes_backend.settings import get_settings
from pydantic import validator


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: str
    username: str
    email: str | None = None


class RegistrationForm(BaseModel):
    username: str
    password: str

    @validator("password")
    def validate_password(cls, password):
        settings = get_settings()
        password = settings.PWD_CONTEXT.hash(password)
        return password


settings = get_settings()
auth_router = APIRouter(tags=["Authentication"])
oauth2bearer = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def create_token(**kwargs):
    payload = kwargs.copy()
    expire_date = datetime.utcnow() + settings.EXPIRY_TIMEDELTA
    payload.update({"exp": expire_date})
    token = jwt.encode(payload, key=settings.JWT_KEY)
    return token


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth: AuthServiceInterface = Depends(auth_service),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await auth.get_user(username)
    if user is None:
        raise credentials_exception
    return user


@auth_router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "Incorrect params"}},
)
async def get_token(
    _: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    auth: AuthServiceInterface = Depends(auth_service),
):
    try:
        user = await auth.authenticate_user(form.username, form.password)
    except exc.WrongPassword:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except exc.NotRegistered:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_token(username=user.username)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Incorrect params"}},
)
async def register(
    _: Request,
    data: RegistrationForm,
    auth: AuthServiceInterface = Depends(auth_service),
) -> None:
    username, password = data.username, data.password
    try:
        await auth.registrate_user(username, password)
    except exc.AlreadyRegistered as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=repr(e))


@auth_router.get(
    "/whoami",
    status_code=status.HTTP_200_OK,
    response_model=User,
    responses={status.HTTP_401_UNAUTHORIZED: {"detail": "Unauthorized"}},
)
async def get_current_user_info(_: Request, current_user=Depends(get_current_user)):
    return User(id=current_user.id, username=current_user.username)
