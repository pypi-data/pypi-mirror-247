# -*- coding: utf-8 -*-
import json
from os import getenv

from dotenv import load_dotenv
from pytest import mark

from kami_messenger.email_messenger import EmailMessenger

load_dotenv()


@mark.skip(reason='Needs to create fixtures to test without real values')
class TestEmailMessenger:
    data = f"""{{
      "name":"Gmail",
      "messages":[{{
          "sender":"dev@kamico.com.br",
          "recipients":["maicon@kamico.com.br"],
          "subject":"Teste",
          "body":"<p>Teste de mensagem</p>",
          "type":"text"
        }}],
      "credentials":{{
          "login":"{getenv("EMAIL_USER")}",
          "password":"{getenv("EMAIL_PASSWORD")}"
      }},
      "engine":""
    }}"""

    def test_when_email_get_valid_json_data_then_returns_new_email_messenger(
        self,
    ):
        json_data = json.loads(self.data)
        new_email_messenger = EmailMessenger(**json_data)
        assert json_data == new_email_messenger.dict()

    def test_when_email_sucess_connect_should_returns_200(self):
        json_data = json.loads(self.data)
        new_email_messenger = EmailMessenger(**json_data)
        status = new_email_messenger.connect()

        assert status == 200

    def test_when_connect_email_should_update_engine(self):
        json_data = json.loads(self.data)
        new_email_messenger = EmailMessenger(**json_data)
        new_email_messenger.connect()

        assert new_email_messenger.engine != None

    def test_when_send_message_by_email_should_return_sent_messages_quantity(
        self,
    ):
        json_data = json.loads(self.data)
        new_email_messenger = EmailMessenger(**json_data)
        messages_to_send = len(new_email_messenger.messages)
        sent_messages = new_email_messenger.sendMessage()

        assert messages_to_send == sent_messages
