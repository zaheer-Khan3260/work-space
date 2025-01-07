from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import os
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError
from app.schema import userSchema
from app.utils.exceptions import custom_Exception
from app.dependencies.dependencies import get_user

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET")
ALGORITHM = "HS256"

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
      
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise custom_Exception.credentials_exception()
        token_data = userSchema.TokenData(email=username)
    except InvalidTokenError:
        raise custom_Exception.credentials_exception()
    user = get_user(username=token_data.username)
    if user is None:
        raise custom_Exception.credentials_exception()
    return user