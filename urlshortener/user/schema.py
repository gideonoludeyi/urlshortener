from pydantic import BaseModel, Field


class User(BaseModel):
    email: str = Field(title="The email of the user which is unique")


class UserInDB(User):
    hashed_password: str = Field(title="The hash of the user's password")
    ignore_access_tokens_before: int = Field(
        default=0, title="The time of the user's last logout action. Helps to invalidate access tokens issued before the the time.")
