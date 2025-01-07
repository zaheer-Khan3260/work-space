from fastapi import HTTPException, status # type: ignore


class custom_Exception():
    def userExist_exception(self):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    def userNotFound_exception(self):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    def credentials_exception(self):
        return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Password is incorrect",
        headers={"WWW-Authenticate": "Bearer"},
        )
    
    def token_creation_exception(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to Create Token",
            headers={"WWW-Authenticate": "Bearer"},
        )

