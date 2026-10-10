from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from apps.schemas import UserCreate, UserResponse, UserLogin,LoginResponse
from apps.database import get_db
from sqlalchemy.orm import Session
from apps.models import User
from passlib.context import CryptContext
from sqlalchemy import or_
from jose import jwt
from datetime import datetime, timedelta,timezone
from apps.config import settings
from fastapi.security import OAuth2PasswordBearer

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.get("/me", response_model=UserResponse, summary="Get current user", description="Endpoint to get the currently authenticated user's information")
def get_current_user(token: str = Depends(OAuth2_scheme), db: Session = Depends(get_db)):
    email=verify_token(token, db)
    return {"email": email}

@router.post("/signup", response_model=UserResponse, summary="User signup", description="Endpoint for user registration")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Here you would typically add logic to create a new user in the database
    # For demonstration purposes, we'll just return the user data with a mock ID
    existing_user = db.query(User).filter(
        or_( User.username == user.username, User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")

    hashed_password = crypt_context.hash(user.password[:72])
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=LoginResponse, summary="User login", description="Endpoint for user login")
def login(form_data:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    # Here you would typically add logic to authenticate the user
    # For demonstration purposes, we'll just return the user data with a mock ID

    db_user = db.query(User).filter(User.username ==form_data.username).first()
    if not db_user or not crypt_context.verify(form_data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    #JWT token generation logic would go here
    token=jwt.encode(
        {
            "sub": db_user.email,
            "exp": datetime.now(timezone.utc) + timedelta(days=1)
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return {"user": db_user, "access_token": token, "token_type": "bearer"}

@router.get("/verify_token", response_model=UserResponse, summary="Get current user", description="Endpoint to get the currently authenticated user's information")
def verify_token(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    db_user = db.query(User).filter(User.email == email).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return db_user