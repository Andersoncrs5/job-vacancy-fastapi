import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from typing import Final

load_dotenv()

SCHEMES: Final[str | None] = os.getenv("SCHEMES") 
DEPRECATED: Final[str | None] = os.getenv("DEPRECATED")
ROUNDS: Final[str | None] = os.getenv("ROUNDS")

if SCHEMES is None or DEPRECATED is None or ROUNDS is None:
    raise ValueError("SCHEMES, ROUNDS or DEPRECATED are not configured")

pwd_context: Final[CryptContext] = CryptContext(
    schemes=[SCHEMES], 
    deprecated=DEPRECATED,
    bcrypt__rounds=int(ROUNDS) 
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)    