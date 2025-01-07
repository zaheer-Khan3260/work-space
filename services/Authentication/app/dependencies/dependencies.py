from fastapi import Depends
from app.utils.jwtToken import verify_password
from sqlalchemy.orm import Session
from app.db.database import sessionLocal
from app.auth.models.authModel import Auth


def get_db() -> Session:
    db = sessionLocal()
    try:
        yield db
    except Exception as e:  
        print(f"Error in get_db: {e}")  
        raise  
    finally:
        db.close()

        
        
def get_user(email: str, db: Session = Depends(get_db)):
    try:
        return db.query(Auth).filter(Auth.email == email).first()
    except Exception as e:
        print(f"Error while validate email: {e}")
        raise e

def authenticate_user(email: str, password: str, db : Session = Depends(get_db)):
    try:
        user = get_user(email=email, db=db)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
    except Exception as e:
        print(f"Error in authenticate_user: {e}")
        raise e


