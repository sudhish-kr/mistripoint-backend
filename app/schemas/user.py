from pydantic import BaseModel, field_validator

class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
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