from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from maddie.dependency_container import DependencyContainer

T = TypeVar('T')


class Dependency(ABC, Generic[T]):
    @staticmethod
    @abstractmethod
    def create(dependency_container: DependencyContainer) -> T:
        pass
