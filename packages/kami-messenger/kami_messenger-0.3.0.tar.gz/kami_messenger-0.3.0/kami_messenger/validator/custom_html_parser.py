# -*- coding: utf-8 -*-
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.start_tags = list()
        self.end_tags = list()
        self.attributes = list()

    def is_text_html(self):
        return len(self.start_tags) == len(self.end_tags)

    def handle_starttag(self, tag, attrs):
        self.start_tags.append(tag)
        self.attributes.append(attrs)

    def handle_endtag(self, tag):
        self.end_tags.append(tag)

    def handle_data(self, data):
        print('Encountered some data  :', data)
