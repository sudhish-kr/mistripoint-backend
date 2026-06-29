from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.user import User
from app.models.service_request import ServiceRequest
from app.schemas.user import (
    RegisterSchema,
    LoginSchema,
    ServiceRequestSchema,
    ForgotPasswordSchema,
    AddToCartSchema,
    AddressSchema
)
from app.schemas.user import UpdateBookingStatusSchema
from app.schemas.user import UpdateStatusSchema
from app.models.service_request import ServiceRequest
from app.models.category import Category
router = APIRouter(prefix="/auth", tags=["Authentication"])
from app.models.cart import CartItem
from app.schemas.user import AddToCartSchema
from app.models.booking import Booking
from app.models.booking_item import BookingItem
from app.models.cart import CartItem
from app.models.service import Service
from app.schemas.user import CreateBookingSchema
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

@router.get("/all-customers")
def all_customers():

    db = SessionLocal()

    users = db.query(User).all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "city": user.city,
            "address": user.address,
            "pincode": user.pincode
        })

    return {
        "total_customers": len(result),
        "customers": result
    }

@router.get("/categories")
def get_categories():

    db = SessionLocal()

    categories = db.query(Category).all()

    return categories

@router.post("/cart/add/{user_id}")
def add_to_cart(user_id: int, data: AddToCartSchema):

    db = SessionLocal()

    item = CartItem(
        customer_id=user_id,
        service_id=data.service_id,
        quantity=data.quantity
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "message": "Added to cart",
        "cart_id": item.id
    }

@router.get("/cart/{user_id}")
def get_cart(user_id: int):

    db = SessionLocal()

    items = db.query(CartItem, Service).join(
        Service,
        CartItem.service_id == Service.id
    ).filter(
        CartItem.customer_id == user_id
    ).all()

    result = []

    for cart_item, service in items:
        result.append({
            "cart_id": cart_item.id,
            "service_name": service.name,
            "price": float(service.price),
            "quantity": cart_item.quantity,
            "total": float(service.price) * cart_item.quantity
        })

    return result

@router.post("/address/{user_id}")
def add_address(user_id: int, data: AddressSchema):

    db = SessionLocal()

    new_address = Address(
        customer_id=user_id,
        full_name=data.full_name,
        phone=data.phone,
        address=data.address,
        city=data.city,
        pincode=data.pincode
    )

    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return {
        "message": "Address Added Successfully",
        "address_id": new_address.id
    }

@router.get("/address/{user_id}")
def get_address(user_id: int):

    db = SessionLocal()

    addresses = db.query(Address).filter(
        Address.customer_id == user_id
    ).all()

    return addresses

@router.post("/create-booking/{user_id}")
def create_booking(user_id: int, data: CreateBookingSchema):

    db = SessionLocal()

    # User ke cart ke items nikalo
    cart_items = db.query(CartItem).filter(
        CartItem.customer_id == user_id
    ).all()

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    # Booking create karo
    booking = Booking(
        customer_id=user_id,
        address_id=data.address_id,
        status="Pending"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    # Cart ke items booking_items me save karo
    for item in cart_items:

        service = db.query(Service).filter(
            Service.id == item.service_id
        ).first()

        booking_item = BookingItem(
            booking_id=booking.id,
            service_id=item.service_id,
            quantity=item.quantity,
            price=service.price
        )

        db.add(booking_item)

    db.commit()

    # Cart empty karo
    db.query(CartItem).filter(
        CartItem.customer_id == user_id
    ).delete()

    db.commit()

    return {
        "message": "Booking Created Successfully",
        "booking_id": booking.id
    }

@router.put("/update-status/{booking_id}")
def update_status(booking_id: int, data: UpdateStatusSchema):

    db = SessionLocal()

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    booking.status = data.status

    db.commit()
    db.refresh(booking)

    return {
        "message": "Status Updated Successfully",
        "booking": booking
    }

@router.put("/admin/update-booking-status/{booking_id}")
def update_booking_status(
    booking_id: int,
    data: UpdateBookingStatusSchema
):
    db = SessionLocal()

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    allowed_status = [
        "Pending",
        "Approved",
        "Rejected",
        "On The Way",
        "Completed",
        "Cancelled"
    ]

    if data.status not in allowed_status:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    booking.status = data.status

    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking status updated successfully",
        "booking_id": booking.id,
        "status": booking.status
    }