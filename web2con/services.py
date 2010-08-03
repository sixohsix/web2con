
from .api import Web2Connector

class Twitter(Web2Connector):
    def __init__(self):
        Web2Connector.__init__(self, domain="api.twitter.com")
