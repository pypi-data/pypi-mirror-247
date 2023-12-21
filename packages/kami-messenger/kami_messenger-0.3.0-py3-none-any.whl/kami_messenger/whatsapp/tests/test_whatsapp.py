# -*- coding: utf-8 -*-
import json
from os import getenv

from dotenv import load_dotenv
from pytest import mark

from kami_messenger.whatsapp import Whatsapp

load_dotenv()


@mark.skip(reason='Defined but not implemented')
class TestWhatsapp:
    data = f"""{{
      "name":"Whatsapp",
      "messages":[{{
          "sender":"",
          "recipients":["21983144824"],
          "subject":"Teste",
          "body":"<p>Teste de mensagem</p>"
        }}],
      "credentials":{{" implementar o dicionário das credenciais necessárias para acessar o whatsapp usando getenv() para proteção dos dados ": "valor"}},
      "engine":null
    }}"""

    def test_when_email_get_valid_json_data_then_returns_new_whatsapp_messenger(
        self,
    ):
        json_data = json.loads(self.data)
        new_whatsapp_messenger = Whatsapp(**json_data)
        assert json_data == new_whatsapp_messenger.dict()

    def test_when_whatsapp_sucess_connect_should_returns_200(self):
        json_data = json.loads(self.data)
        new_whatsapp_messenger = Whatsapp(**json_data)
        status = new_whatsapp_messenger.connect()

        assert status == 200

    def test_when_connect_whatsapp_should_update_engine(self):
        json_data = json.loads(self.data)
        new_whatsapp_messenger = Whatsapp(**json_data)
        new_whatsapp_messenger.connect()

        assert new_whatsapp_messenger.engine != None

    def test_when_send_message_by_whatsapp_should_return_sent_messages_quantity(
        self,
    ):
        json_data = json.loads(self.data)
        new_whatsapp_messenger = Whatsapp(**json_data)
        messages_to_send = len(new_whatsapp_messenger.messages)
        sent_messages = new_whatsapp_messenger.sendMessage()

        assert messages_to_send == sent_messages
