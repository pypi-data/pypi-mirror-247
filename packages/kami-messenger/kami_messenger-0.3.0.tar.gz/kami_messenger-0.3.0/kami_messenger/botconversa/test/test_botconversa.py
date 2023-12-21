# -*- coding: utf-8 -*-
import json

from dotenv import load_dotenv
from pytest import mark

from kami_messenger.botconversa import Botconversa

load_dotenv()


@mark.skip(reason='Defined but not implemented')
class TestBotconversa:
    data = f"""{{
      "name":"Botconversa",
      "messages":[{{
          "sender":"+5511916654692",
          "recipients":["+5521983144824"],
          "subject":"Teste",
          "body":"<p>Teste de mensagem</p>",
          "type":"text"
          }}],          
      "credentials":{{"api-key": "b6ba8d5c-19a1-4c38-8f5b-3966f11f2bbe"}},
      "engine":null
    }}"""

    def test_when_email_get_valid_json_data_then_returns_new_botconversa_messenger(
        self,
    ):
        json_data = json.loads(self.data)
        new_botconversa_messenger = Botconversa(**json_data)
        assert json_data == new_botconversa_messenger.dict()

    def test_when_send_message_by_botconversa_should_return_sent_messages_quantity(
        self,
    ):
        json_data = json.loads(self.data)
        new_botconversa_messenger = Botconversa(**json_data)
        messages_to_send = len(new_botconversa_messenger.messages)
        sent_messages = new_botconversa_messenger.sendMessage()

        assert messages_to_send == sent_messages
