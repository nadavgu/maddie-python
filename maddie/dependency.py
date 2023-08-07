from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class Dependency(ABC, Generic[T]):
    @staticmethod
    @abstractmethod
    def create() -> T:
        pass
