
from .api import Web2Connector, handle_json, handle_str

class Twitter(Web2Connector):
    def __init__(self):
        Web2Connector.__init__(
            self, domain="api.twitter.com", suffix=".json",
            response_handler=handle_json)

class TwitterXml(Web2Connector):
    def __init__(self):
        Web2Connector.__init__(
            self, domain="api.twitter.com", suffix=".xml",
            response_handler=handle_str)

class Soundcloud(Web2Connector):
    def __init__(self):
        Web2Connector.__init__(
            self, domain="api.soundcloud.com", suffix=".json",
            response_handler=handle_json)
