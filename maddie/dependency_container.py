from typing import Any, Dict, TypeVar, Type

from maddie.dependency import Dependency

T = TypeVar('T', bound=Dependency)


class DependencyContainer:
    def __init__(self):
        self.__dependencies: Dict[type, Any] = {}

    def add(self, dependency_type: Type[T], dependency: T):
        self.__dependencies[dependency_type] = dependency

    def add_dependency(self, dependency: T):
        self.add(type(dependency), dependency)

    def get(self, dependency_type: Type[T]) -> T:
        if dependency_type not in self.__dependencies:
            self.add(dependency_type, dependency_type.create())
        return self.__dependencies[dependency_type]
