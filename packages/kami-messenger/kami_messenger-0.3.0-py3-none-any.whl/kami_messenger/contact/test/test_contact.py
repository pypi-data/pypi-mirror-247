# -*- coding: utf-8 -*-
import json

from pytest import mark

from ..contact import Contact


class TestContact:
    json_data = """{
    "name":"Test1",
    "email":"test@test.com",
    "phone":"+5511999999999",
    "id_botconversa":"123574"
  }"""

    def test_when_contact_get_valid_json_data_then_returns_new_contact(self):
        contact_json_data = json.loads(self.json_data)
        new_contact = Contact(**contact_json_data)
        assert contact_json_data == new_contact.dict()

    @mark.skip(reason='Defined but not implemented')
    def test_when_contact_get_invalid_json_data_then_returns_none(self):
        ...
