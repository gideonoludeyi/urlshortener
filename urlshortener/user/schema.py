from pydantic import BaseModel


class User(BaseModel):
    email: str


class UserInDB(User):
    hashed_password: str
    ignore_access_tokens_before: int = 0
