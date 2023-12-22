from urllib.parse import urljoin
from .clients import Clients

import requests


class CRM:
    def __init__(self, hostname, api_key, verify_ssl=True):
        self.hostname = urljoin(hostname.rstrip("/"), "crm/api/v1.0/")
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self._session = requests.session()
        self._session.headers = {"X-Auth-App-Key": self.api_key}

        self.clients = Clients(self)

    def req(self, method, endpoint, **kwargs):
        url = urljoin(self.hostname, endpoint)
        response = self._session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()


