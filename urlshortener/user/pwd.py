from passlib.context import CryptContext  # type: ignore

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return context.hash(password)


def verify_password(password: str, hashed_password: str):
    return context.verify(password, hashed_password)
