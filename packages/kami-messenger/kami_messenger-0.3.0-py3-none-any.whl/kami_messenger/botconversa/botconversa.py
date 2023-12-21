# -*- coding: utf-8 -*-
import json
import logging
import traceback
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv
from kami_logging import benchmark_with, logging_with
from pydantic import validator

from kami_messenger.messenger import (
    MessageNotSendError,
    Messenger,
    RecipientFormatError,
)
from kami_messenger.validator import DataValidator, IdBotconversaMissingError

botconversa_messenger_logger = logging.getLogger('Botconversa Messenger')
load_dotenv()


class Botconversa(Messenger):
    def _validate_message_recipients(self, message):
        for recipient in message.recipients:
            try:
                data = DataValidator(recipient)
                data._isIdBotconversa()
            except IdBotconversaMissingError:
                e = RecipientFormatError(
                    recipient,
                    f'Recipient {recipient} should be an valid botconversa contact',
                )
                botconversa_messenger_logger.error(f'{e.message} - {e.args}')
                raise MessageNotSendError
            except Exception as e:
                botconversa_messenger_logger.error(traceback.format_exc())
            finally:
                return message

    @validator('messages', pre=True, each_item=True)
    @classmethod
    def recipientsValid(cls, message):
        cls._validate_messages_recipients(message)

    @logging_with(botconversa_messenger_logger)
    @benchmark_with(botconversa_messenger_logger)
    def connect(self):
        try:
            engine = None
            # Implementar a conexão com o serviço do botconversa e atualizar a variavel engine com o objeto responsavel por enviar mensagens
        except Exception as e:
            botconversa_messenger_logger.error(traceback.format_exc())
            raise
        else:
            self.engine = engine
            botconversa_messenger_logger.info(f'Success Connected')

    @logging_with(botconversa_messenger_logger)
    @benchmark_with(botconversa_messenger_logger)
    def _getIdBotconversaByPhone(self, phone: str) -> str:
        url = f'https://backend.botconversa.com.br/api/v1/webhook/subscriber/get_by_phone/{phone}/'

        headers = {
            'accept': 'application/json',
            'api-key': self.credentials['api-key'],
            'Content-Type': 'application/json',
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code < 200 or response.status_code > 299:
                raise MessageNotSendError(
                    value=response.status_code,
                    message=f'API Request returns {response.status_code}',
                )

            res_content = json.loads(response.text)
            return res_content['id']
        except Exception as e:
            botconversa_messenger_logger.error(traceback.format_exc())
            raise
        ...

    @logging_with(botconversa_messenger_logger)
    @benchmark_with(botconversa_messenger_logger)
    def _sendMessage(self, message):
        try:
            message_data = {'type': message.type, 'value': message.body}
            for recipient in message.recipients:
                id_botconversa = self._getIdBotconversaByPhone(recipient)
                url = f'https://backend.botconversa.com.br/api/v1/webhook/subscriber/{id_botconversa}/send_message/'

                headers = {
                    'accept': 'application/json',
                    'api-key': self.credentials['api-key'],
                    'Content-Type': 'application/json',
                }
                response = requests.post(
                    url, headers=headers, data=json.dumps(message_data)
                )
                if response.status_code < 200 or response.status_code > 299:
                    raise MessageNotSendError(
                        value=response.status_code,
                        message=f'API Request returns {response.status_code}',
                    )
                botconversa_messenger_logger.info(
                    f'Send message to: {recipient} | Status: {response.status_code}'
                )
                return 200
        except Exception as e:
            botconversa_messenger_logger.error(traceback.format_exc())
            raise
        finally:
            botconversa_messenger_logger.info(
                f'Message Sucessufully Sent To {message.recipients}'
            )
