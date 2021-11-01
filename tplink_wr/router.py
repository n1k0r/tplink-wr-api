from abc import ABC, abstractmethod
import base64
import hashlib
import re

import requests

from . import exceptions
from .parse.html import find_scripts


class RouterInterface(ABC):
    @abstractmethod
    def page(self, name: str, params: dict = {}) -> str:
        pass


class RouterSession(RouterInterface):
    def __init__(self, host: str, username: str, password: str, *, auto_reauth: bool = True, auth_retries: int = 3) -> str:
        self.host = host
        self.auto_reauth = bool(auto_reauth)
        self.auth_retries = max(auth_retries, 0)

        password_hash = hashlib.md5(password.encode()).hexdigest()
        basic_raw = f"{username}:{password_hash}".encode()
        basic_token = base64.b64encode(basic_raw).decode("utf-8")

        self.session = requests.Session()
        self.session.cookies["Authorization"] = f"Basic {basic_token}"
        self.refresh_token()

    def is_session_valid(self) -> bool:
        url = self.page_url("Index")
        resp = self._get(url)
        reauth = self._is_reauth_doc(resp.text)
        return not reauth

    def refresh_token(self):
        attempts = self.auth_retries+1
        for retry in range(attempts):
            resp = self._get(f"{self.base_url()}/userRpm/LoginRpm.htm?Save=Save")

            match = re.search(f"{self.host}/(\w+)/", resp.text)
            if match:
                self.token = match.group(1)
                if self.is_session_valid():
                    return

        raise exceptions.AuthError(f"Failed to get auth token with specified username and password after {attempts} attempts")

    def base_url(self) -> str:
        return f"http://{self.host}"

    def page_url(self, name: str) -> str:
        return f"{self.base_url()}/{self.token}/userRpm/{name}.htm"

    def page(self, name: str, params: dict = {}) -> str:
        retry = False
        while True:
            doc = self._page_load_attempt(name, params)
            if not self._is_reauth_doc(doc):
                break

            if retry or not self.auto_reauth:
                raise exceptions.PageLoadError(f"Failed to load page {name}. Firmware of the router may not support this feature")

            retry = True
            self.refresh_token()

        return doc

    def _page_load_attempt(self, name: str, params: dict = {}) -> str:
        url = self.page_url(name)
        referer = self.page_url("MenuRpm")

        resp = self._get(url, headers={"Referer": referer})
        if resp.status_code != requests.codes.OK:
            raise exceptions.PageLoadError(f"HTTP code {resp.status_code}")

        return resp.text

    def _get(self, *args, **kwargs):
        try:
            return self.session.get(*args, **kwargs)
        except requests.RequestException as e:
            raise exceptions.NetworkError(e)

    REAUTH_SUBSTR = 'cookie="Authorization=;path=/"'

    @classmethod
    def _is_reauth_doc(cls, doc) -> bool:
        first_script = find_scripts(doc)[0]
        return cls.REAUTH_SUBSTR in first_script
