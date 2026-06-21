from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.user import User
from app.models.service_request import ServiceRequest
from app.schemas.user import (
    RegisterSchema,
    LoginSchema,
    ServiceRequestSchema
)
from app.models.service_request import ServiceRequest
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(user: RegisterSchema):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.phone == user.mobile
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Mobile number already registered"
        )

    new_user = User(
        name=f"{user.first_name} {user.last_name}",
        first_name=user.first_name,
        last_name=user.last_name,
        email=f"{user.mobile}@mistripoint.com",
        phone=user.mobile,
        password=user.password,
        city=user.city,
        address=user.address,
        pincode=user.pincode,
        role="customer"
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
        User.phone == user.mobile
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

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role
    }

@router.post("/request-service/{user_id}")
def request_service(user_id: int, data: ServiceRequestSchema):

    db = SessionLocal()

    new_request = ServiceRequest(
        customer_id=user_id,
        worker_type=data.worker_type,
        problem=data.problem
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return {
        "message": "Request Created Successfully",
        "request_id": new_request.id,
        "status": new_request.status
    }


@router.get("/my-requests/{user_id}")
def my_requests(user_id: int):

    db = SessionLocal()

    requests = db.query(ServiceRequest).filter(
        ServiceRequest.customer_id == user_id
    ).all()

    result = []

    for req in requests:
        result.append({
            "request_id": req.id,
            "worker_type": req.worker_type,
            "problem": req.problem,
            "status": req.status
        })

    return result