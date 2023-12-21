# -*- coding: utf-8 -*-

"""
The Messenger Module represents a generic messaging service, used to abstract the characteristics common to all messaging services used in the project.

Classes:
   Message: str Name that identifies the messaging service
   Messenger: List[Message] List of messages to send
   RecipientFormatError: Custom error that is raised when a recipients doesn't have the rigth format.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, validator


class RecipientFormatError(Exception):
    """
    Custom error that is raised when a recipients doesn't have the rigth format.

    Attributes:
        value: Exception value error
        message: Error message
    """

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class MessageNotSendError(Exception):
    """Custom error that is raised when a message is not sended to a recipient."""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class Message(BaseModel):
    """
    Represents a generic message used in all messengers.

    Attributes:
        sender: Contact of the sender of the message
        recipients: List of contacts who will receive the message
        subject: Message subject is optional
        body: message body, content that will be sent to recipients
    """

    sender: str
    recipients: List[str]
    subject: Optional[str]
    body: str
    type: str = 'text'


class Messenger(ABC, BaseModel):
    """
    Represents a generic messaging service, used to abstract the characteristics common to all messaging services used in the project.

    Attributes:
        name: str Name that identifies the messaging service
        messages: List[Message] List of messages to send
        credentials: Dict Dictionary with the information needed to connect the service
        engine: Any Object that contains methods for sending messages
    """

    name: str
    messages: List[Message] = []
    credentials: Dict
    engine: Any = None

    @abstractmethod
    def _validate_message_recipients(message: Message) -> Message:
        """
        Checks whether the recipients of a given message are valid using validator module and pydantic validation especfications. The type of recipient changes according to the used messenger

        Args:
            message: Individual message to check recipients

        Returns:
            The given message if all recipients is valid

        Raises:
            RecipientFormatError: If at least one of the recipients is not valid.
        """
        ...

    @classmethod
    @abstractmethod
    def recipientsValid(cls, message: Message):
        """
        Calls _validate_message_recipients to check whether the recipients of a all messages in the messenger are valids. Uses pydantic validator decorator to iterate over all messages

        Args:
            message: Message to check recipients

        Raises:
            RecipientFormatError: If at least one of the recipients is not valid.
        """
        ...

    @abstractmethod
    def connect(self) -> int:
        """
        Connect with the messaging service using self.credentials for the necessary information to connect (eg Login and Password or API-Token) and updates the 'engine' attribute with the service created for sending messages if any success.

        Returns:
            An integer that represents the status code obeying the http service status code standard (eg: 200 to success and 404 to not found error).

        Raises:
            Exception: If there is any problem with the service trying to connect
        """
        ...

    @abstractmethod
    def _sendMessage(
        self, message: Message, attachments: List[str] = None
    ) -> int:
        """
        Helper method that implements sending a single message to its recipients

        Args:
            message: Individual message to sent to all recipients

        Returns:
            An integer that represents the status code obeying the http service status code standard (eg: 200 to success and 404 to not found error).

        Raises:
            Exception: If there is any problem with the service trying to send message.
        """
        ...

    def sendMessage(self, messages: List[Message] = None, attachments: List[str] = None) -> int:
        """
        Calls _sendMessage to send all messages from a list to their respective recipients, if it does not receive a list as a parameter it sends all messages belonging to the messages attribute

        Args:
            messages: A list of Individual messages to send, it's optional

        Returns:
            An integer that's represents the amount of sent messages

        Raises:
            Exception: If there is any problem with the service trying to send message.
        """

        sent_messages = 0
        selected_messages = self.messages
        if messages:
            selected_messages = messages

        for message in selected_messages:
            try:
                sent_messages += 1 if self._sendMessage(message, attachments) == 200 else 0
            except Exception as e:
                raise e

        return sent_messages
