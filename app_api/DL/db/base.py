from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AbstractDB(ABC):
    @abstractmethod
    def create_scheme(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_session(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def dispose(self) -> None:
        raise NotImplementedError


