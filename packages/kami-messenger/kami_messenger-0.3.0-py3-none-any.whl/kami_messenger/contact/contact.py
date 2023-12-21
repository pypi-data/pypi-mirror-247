# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, root_validator, validator

from kami_messenger.validator import (
    DataValidator,
    EmailFormatError,
    PhoneFormatError,
)


class ContactMissingError(Exception):
    """Custom error that is raised when a contact doesn't have any of the contact methods."""

    def __init__(self, name: str, message: str) -> None:
        self.name = name
        self.message = message
        super().__init__(message)


class Contact(BaseModel):
    name: str
    email: Optional[str]
    phone: Optional[str]
    id_botconversa: Optional[str]

    @root_validator(pre=True)
    @classmethod
    def checkAtLeastOneContact(cls, values):
        """Make sure there is at least one of the contact fields options are defined."""

        if (
            'email' not in values
            and 'phone' not in values
            and 'id_botconversa' not in values
        ):
            raise ContactMissingError(
                name=values['name'],
                message='Contacts must have at least one of these contact methods [email, phone, id_botconversa]',
            )
        return values

    @validator('phone')
    @classmethod
    def phoneValid(cls, value):
        data = DataValidator(value)
        if not data.isPhone():
            raise PhoneFormatError(
                value=value, message="It's Not a Valid Phone Number"
            )
        return value

    @validator('email')
    @classmethod
    def emailValid(cls, value):
        data = DataValidator(value)
        if not data.isEmail():
            raise EmailFormatError(
                value=value, message="It's Not a Valid Email Address."
            )
        return value
