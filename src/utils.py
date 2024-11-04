from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def validate_list(values, class_type):
    return [class_type.model_validate(obj) for obj in values]


async def validate(value, class_type):
    return class_type.model_validate(value)
