from pydantic import BaseModel, field_validator



class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    mobile: str
    password: str
    city: str
    address: str
    pincode: str

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value):
        if not value.isdigit():
            raise ValueError("Mobile number must contain only digits")

        if len(value) != 10:
            raise ValueError("Mobile number must be exactly 10 digits")

        return value


class LoginSchema(BaseModel):
    mobile: str
    password: str

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value):
        if not value.isdigit():
            raise ValueError("Mobile number must contain only digits")

        if len(value) != 10:
            raise ValueError("Mobile number must be exactly 10 digits")

        return value


class ForgotPasswordSchema(BaseModel):
    mobile: str
    new_password: str

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value):
        if not value.isdigit():
            raise ValueError("Mobile number must contain only digits")

        if len(value) != 10:
            raise ValueError("Mobile number must be exactly 10 digits")

        return value

class ServiceRequestSchema(BaseModel):
    worker_type: str
    problem: str

class AddToCartSchema(BaseModel):
    service_id: int
    quantity: int = 1

class AddressSchema(BaseModel):
    full_name: str
    phone: str
    address: str
    city: str
    pincode: str

class CreateBookingSchema(BaseModel):
    address_id: int

class UpdateStatusSchema(BaseModel):
    status: str

class UpdateBookingStatusSchema(BaseModel):
    status: str