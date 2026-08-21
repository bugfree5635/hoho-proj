from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_database
from app.database.models import User
from app.schemas.user import UserCreate, UserLogin
from app.security.auth import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_database)):

    new_user = User(
        username=user.username, hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "user created"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_database)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="invalid username or password",
        )

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="invalid username or password",
        )

    token = create_access_token({"sub": db_user.username})

    return {"access_token": token, "token_type": "bearer"}
