from pwdlib import PasswordHash
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

import jwt

load_dotenv()
password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXP_MINUTES = 30


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str
) -> bool:
    return password_hash.verify(
        password,
        hashed_password
    )

def create_access_token(user_id: str, role: str) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_EXP_MINUTES
    )

    payload = {
        "sub": user_id,
        "role": role,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

def decode_access_token(token: str) -> dict:

    try:

        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

def require_role(required_role: str):

    def role_checker(
        token: str = Depends(oauth2_scheme)
    ):

        payload = decode_access_token(token)

        if payload.get("role") != required_role:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )

        return payload

    return role_checker