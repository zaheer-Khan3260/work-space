from pydantic import BaseModel


class UserData(BaseModel):
    name: str
    date_of_birth: str
    organization: str
    position: str

class TokenData(BaseModel):
    email: str | None = None

