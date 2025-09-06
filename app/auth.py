from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, auth, models

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", response_model=schemas.UserOut)
def register(payload: schemas.RegisterRequest, db: Session = Depends(database.get_db)):
    hashed_password = auth.get_password_hash(payload.password)
    user = models.User(
        name=payload.name,
        email=payload.email,
        password=hashed_password,
        role=payload.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginSchema, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not auth.verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"id": user.id})
    return {"access_token": token, "token_type": "bearer"}
