from typing import Any, Dict, TypeVar, Type, Callable

T = TypeVar('T')


class DependencyContainer:
    def __init__(self):
        self.__dependencies: Dict[type, Any] = {}
        self.__providers: Dict[type, Callable[['DependencyContainer'], Any]] = {}

    def add(self, dependency_type: Type[T], dependency: T):
        self.__dependencies[dependency_type] = dependency

    def add_dependency(self, dependency: T):
        self.add(type(dependency), dependency)

    def get(self, dependency_type: Type[T]) -> T:
        if dependency_type not in self.__dependencies:
            self.add(dependency_type, dependency_type.create(self))
        return self.__dependencies[dependency_type]

    def add_provider(self, dependency_type: Type[T], provider: Callable[['DependencyContainer'], Any]):
        self.__providers[dependency_type] = provider

    def bind(self, dependency_type: Type[T], providing_type: Type[T]):
        self.add_provider(dependency_type, lambda dependency_container: dependency_container.get(providing_type))
