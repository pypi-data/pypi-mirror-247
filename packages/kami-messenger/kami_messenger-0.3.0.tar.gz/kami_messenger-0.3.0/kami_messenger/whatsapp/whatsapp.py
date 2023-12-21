# -*- coding: utf-8 -*-
import logging
import traceback
from os import getenv

from dotenv import load_dotenv
from kami_logging import benchmark_with, logging_with
from pydantic import validator

from kami_messenger.messenger import Messenger, RecipientFormatError
from kami_messenger.validator import DataValidator, PhoneFormatError

whatsapp_messenger_logger = logging.getLogger('Whatsapp Messenger')


class Whatsapp(Messenger):
    def _validate_messages_recipients(message):
        for recipient in message.recipients:
            try:
                data = DataValidator(recipient)
                data.isPhone()
            except PhoneFormatError:
                e = RecipientFormatError(
                    recipient,
                    f'Recipient {recipient} should be an valid phone number',
                )
                whatsapp_messenger_logger.error(f'{e.message} - {e.args}')
                raise
            except Exception as e:
                whatsapp_messenger_logger.error(traceback.format_exc())
            finally:
                return message

    @validator('messages', pre=True, each_item=True)
    @classmethod
    def recipientsValid(cls, message):
        cls._validate_message_recipients(message)

    @logging_with(whatsapp_messenger_logger)
    @benchmark_with(whatsapp_messenger_logger)
    def connect(self):
        try:
            engine = None
            # Implementar a conexão com o serviço do whatsapp e atualizar a variavel engine com o objeto responsavel por enviar mensagens
        except Exception as e:
            whatsapp_messenger_logger.error(traceback.format_exc())
            raise
        else:
            self.engine = engine
            whatsapp_messenger_logger.info(f'Success Connected')

    @logging_with(whatsapp_messenger_logger)
    @benchmark_with(whatsapp_messenger_logger)
    def _sendMessage(self, message):
        try:
            self.connect()
            # Implementar o envio de mensagens pelo botconversa usando o atributo 'engine'
            # Exemplo: self.engine.send_message()
            ...
        except Exception as e:
            whatsapp_messenger_logger.error(traceback.format_exc())
            raise
        finally:
            whatsapp_messenger_logger.info(
                f'Message Sucessufully Sent To {message.recipients}'
            )
