from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import RegisterSchema, LoginSchema, UpdateUserSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(user: RegisterSchema):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.mobile == user.mobile
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Mobile number already registered"
        )

    new_user = User(
        mobile=user.mobile,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Registered Successfully",
        "id": new_user.id
    }


@router.post("/login")
def login(user: LoginSchema):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.mobile == user.mobile
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.password != existing_user.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    return {
        "message": "Login Successful",
        "user_id": existing_user.id
    }

@router.get("/customers/{user_id}")
def get_customer(user_id: int):

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return user

@router.get("/customers")
def get_customers():

    db = SessionLocal()

    users = db.query(User).all()

    return users


@router.put("/customers/{user_id}")
def update_customer(
    user_id: int,
    updated_user: UpdateUserSchema
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    user.mobile = updated_user.mobile

    db.commit()
    db.refresh(user)

    return {
        "message": "Customer updated successfully",
        "user": user
    }