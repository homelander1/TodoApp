from datetime import timedelta, datetime, timezone
from fastapi import HTTPException

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from models import Users
from sqlalchemy.orm import Session
from starlette import status
from passlib.context import CryptContext
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette.status import HTTP_401_UNAUTHORIZED

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'aldfa7sfdja8faowi3rjaf3a3'
ALGORYTHM = 'HS256'

brecypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number:str

class Token(BaseModel):
    access_token:str
    token_type:str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username:str, password:str, db):
    user=db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not brecypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username:str, user_id:int,role:str, expires_delta:timedelta):
    encode = {'sub':username, 'id': user_id, 'role':role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORYTHM)

async def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM])
        username:str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role:str=payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code = HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
        return {'username':username, 'id':user_id, 'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code = HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request: CreateUserRequest):

    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=brecypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()

# @router.get("/", status_code=status.HTTP_200_OK)
# async def get_users(db:db_dependency):
#     return db.query(Users).all()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user=authenticate_user(form_data.username, form_data.password, db)
    if not user or user is None:
        raise HTTPException(status_code = HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    token = create_access_token(user.username, user.id,user.role, timedelta(minutes=20) )
    return {'access_token':token, 'token_type':'bearer'}

