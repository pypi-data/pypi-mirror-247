import re
from os import getenv
from urllib.parse import urljoin

import phonenumbers as phonevalidator
import requests
from dotenv import load_dotenv

from .custom_html_parser import MyHTMLParser

load_dotenv()


class PhoneFormatError(Exception):
    """Custom error that is raised when a phone number doesn't have the rigth format."""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class EmailFormatError(Exception):
    """Custom error that is raised when a email address doesn't have the rigth format."""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class HTMLFormatError(Exception):
    """Custom error that is raised when a html document doesn't have the rigth format."""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class IdBotconversaMissingError(Exception):
    """Custom error that is raised when a id to botconversa contact doesn't exist."""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class DataValidator:
    def __init__(self, value: str):
        self.value = value

    def isPhone(self):
        phone = phonevalidator.parse(self.value)
        if not phonevalidator.is_valid_number(phone):
            raise PhoneFormatError(
                value=self.value, message="It's Not A Valid Phone Number."
            )

        return True

    def isEmail(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not (re.fullmatch(regex, self.value)):
            raise EmailFormatError(
                value=self.value, message="It's Not A Valid Email Address."
            )

        return True

    def isHtml(self):
        parser = MyHTMLParser()
        parser.feed(self.value)
        if not parser.is_text_html():
            raise HTMLFormatError(
                value=self.value, message="It's Not A Valid HTML document."
            )

        return True

    def _isIdBotconversa(self):
        api_url = f'https://backend.botconversa.com.br/api/v1/webhook/subscriber/get_by_phone/{self.value}/'

        headers = {
            'accept': 'application/json',
            'api-key': getenv('BOTCONVERSA_API_TOKEN'),
            'Content-Type': 'application/json',
        }
        response = requests.get(api_url, headers=headers)
        if response.status_code < 200 or response.status_code >= 400:
            raise IdBotconversaMissingError(
                value=self.value,
                message="It's Not A Valid IdBotconversa User.",
            )

        return True
