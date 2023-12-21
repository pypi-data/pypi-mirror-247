# -*- coding: utf-8 -*-
import json

from pytest import mark

from ..messenger import Message, Messenger


class TestMessage:
    data = """{
        "sender":"dev@kamico.com.br",
        "recipients":["maicon@kamico.com.br"],
        "subject":"Teste",
        "body":"<p>Teste de mensagem</p>",
        "type":"text"
    }"""

    def test_when_message_get_valid_json_data_then_returns_new_message(self):
        json_data = json.loads(self.data)
        new_message = Message(**json_data)
        assert json_data == new_message.dict()

    @mark.skip(reason='Defined but not implemented')
    def test_when_message_get_invalid_json_data_then_raise_exception(self):
        pass
