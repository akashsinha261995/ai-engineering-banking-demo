from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from backend.security import (
    verify_password,
    create_access_token,
)
from backend.database import get_db
from backend.models import User
from backend.security import hash_password


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    user = User(
        id=username,
        username=username,
        password_hash=hash_password(password)
    )

    db.add(user)
    db.commit()

    return {
        "message": "User registered successfully",
        "username": username
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.username == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        user.id,
        user.role
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }




