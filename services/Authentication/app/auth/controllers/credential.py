from datetime import timedelta
from http.client import HTTPException
from typing import Annotated
from fastapi import status, APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.dependencies import authenticate_user, get_db, get_user
from sqlalchemy.orm import Session 
from app.auth.models.authModel import Auth 
from app.utils.jwtToken import get_password_hash, verify_password, create_access_token
from app.utils.exceptions import custom_Exception
from app.schema import authSchema

router = APIRouter(
    tags=["auth"],
    prefix="/auth"
    )

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(user: authSchema.CreateUser, db: Session = Depends(get_db)):
    
    user_obj = authSchema.CreateUser(**user.dict())
    user_exist = get_user(user_obj.email, db)
    
    if user_exist:
        raise custom_Exception.userExist_exception()
    hash_password = get_password_hash(user_obj.password)
    
    # Save user to database
    try:
        user_obj = Auth(
            email=user_obj.email,
            password=hash_password,
            is_active=True,
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj
    except Exception as e:
        db.rollback()
        raise e
    
    
    
@router.post("/login", status_code=status.HTTP_200_OK)
async def login( user: authSchema.CreateUser, db: Session = Depends(get_db)):
    try:
        user_obj = authSchema.CreateUser(**user.dict())
        user_exist = get_user(user_obj.email, db)
        
        if not user_exist:
            raise custom_Exception.userNotFound_exception()
        passwordverification = verify_password(user_obj.password, user_exist.password)
        if not passwordverification:
            raise custom_Exception.credentials_exception()
        
        access_token = create_access_token(data={"sub": user_obj.email})
        if not access_token:
            raise custom_Exception.token_creation_exception()
        
        return authSchema.Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        print(f"Error in login: {e}") 
        raise e



# @router.post("/token", status_code=status.HTTP_200_OK)
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#     db: Session = Depends(get_db)
# ) -> authSchema.Token:
    
#     user = authenticate_user(email=form_data.username, password=form_data.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=15)
#     access_token = create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )
#     return authSchema.Token(access_token=access_token, token_type="bearer")



