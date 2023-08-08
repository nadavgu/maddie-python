from typing import Any, Dict, TypeVar, Type, Callable, Tuple, Optional

T = TypeVar('T')
Tag = Any
DependencyID = Tuple[Type, Tag]


class DependencyContainer:
    def __init__(self):
        self.__dependencies: Dict[DependencyID, Any] = {}
        self.__providers: Dict[DependencyID, Callable[['DependencyContainer'], Any]] = {}

    def add(self, dependency_type: Type[T], dependency: T, tag: Tag = None):
        self.__dependencies[(dependency_type, tag)] = dependency

    def add_dependency(self, dependency: T, tag: Tag = None):
        self.add(type(dependency), dependency, tag)

    def get(self, dependency_type: Type[T], tag: Tag = None) -> T:
        if (dependency_type, tag) not in self.__dependencies:
            self.add(dependency_type, self.create(dependency_type, tag), tag)
        return self.__dependencies[(dependency_type, tag)]

    def create(self, dependency_type: Type[T],  tag: Tag = None) -> T:
        if (dependency_type, tag) in self.__providers:
            return self.__providers[(dependency_type, tag)](self)
        return dependency_type.create(self)

    def add_provider(self, dependency_type: Type[T], provider: Callable[['DependencyContainer'], Any],
                     tag: Tag = None):
        self.__providers[(dependency_type, tag)] = provider

    def bind(self, dependency_type: Type[T], providing_type: Type[T], tag: Tag = None):
        self.add_provider(dependency_type, lambda dependency_container: dependency_container.get(providing_type), tag)
