# -*- coding: utf-8 -*-
from os.path import isfile, split
from typing import List

from jinja2 import Environment, FileSystemLoader
from jinja2 import Template as Jtemplate
from pydantic import BaseModel

from kami_messenger.contact import Contact
from kami_messenger.messenger import Message, Messenger


class KamiMessenger(BaseModel):
    messengers: List[Messenger]
    messages: List[Message]
    contacts: List[Contact]
    status: str = None

    def _setMessageTemplateFromFile(self, template):
        template_folder, template_file = (
            template_folder,
            template_file,
        ) = split(template)
        loader = FileSystemLoader(template_folder)
        enviroment = Environment(loader=loader)
        message_template = enviroment.get_template(template_file)
        self.message.body = message_template.render(self.contact)

    def _setMessageTemplateFromStr(self, template):
        message_template = Jtemplate(template)
        self.message.body = message_template.render(self.contact)

    def _getMessengerByName(self, messenger_name):
        return [
            messenger
            for messenger in self.messengers
            if messenger.name == messenger_name
        ][0]

    def setMessageTemplate(self, template):
        if isfile(template):
            self._setMessageTemplateFromFile(template)
        elif isinstance(template, str):
            self._setMessageTemplateFromFile(template)

    def setNewMessenger(self, messenger):
        if isinstance(messenger, Messenger):
            self.messengers.append(messenger)

    def sendMessageBy(self, messenger_name=None, messages=None):
        selected_messenger = self.messengers[0]
        selected_messages = self.messages

        if messenger_name:
            selected_messenger = self._getMessengerByName(messenger_name)

        if messages:
            selected_messages = messages

        selected_messenger.sendMessage(selected_messages)
