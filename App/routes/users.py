from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app import schemas
from app.models import User
from app.auth import create_access_token, get_current_user, verify_password, hash_password
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already Registered")

    hashed_pass = hash_password(user.password)

    new_user = User(
        email = user.email,
        hashed_password = hashed_pass
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()

    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    access_token = create_access_token(
        data = {"sub":db_user.email}
    )

    return{
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/users/me", response_model=schemas.UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

