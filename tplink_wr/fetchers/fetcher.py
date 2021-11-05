from abc import ABC, abstractmethod
from dataclasses import asdict

from tplink_wr.router import RouterInterface


class Fetcher(ABC):
    @staticmethod
    @abstractmethod
    def fetch(router: RouterInterface):
        pass

    def dict(self):
        return asdict(self)
