from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from fastapi import Depends, HTTPException
from app.models import User
from app.database import SessionLocal

MY_KEY = "my-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated = "auto"
)

def hash_password(password):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(password,hashed_password):
    return pwd_context.verify(password,hashed_password)

def create_access_token(data):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRY)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, MY_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try: 
        payload = jwt.decode(token, MY_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid Credentials")

        db = SessionLocal()
        user = db.query(User).filter(User.email==email).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User Not Found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
