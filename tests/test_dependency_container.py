from dataclasses import dataclass

import pytest

from maddie.dependency import Dependency
from maddie.dependency_container import DependencyContainer

CREATE_VALUE = 1000
ADD_VALUE = 2000
PROVIDE_VALUE = 3000
BOUND_VALUE = 4000


@dataclass
class SimpleDependency(Dependency):
    value: int

    amount_created = 0

    @staticmethod
    def create(dependency_container: DependencyContainer) -> 'SimpleDependency':
        SimpleDependency.amount_created += 1
        return SimpleDependency(value=CREATE_VALUE)

    @staticmethod
    def provide(_: DependencyContainer) -> 'SimpleDependency':
        SimpleDependency.amount_created += 1
        return SimpleDependency(value=PROVIDE_VALUE)


@dataclass
class ComplexDependency(Dependency):
    dependency: SimpleDependency

    @staticmethod
    def create(dependency_container: DependencyContainer) -> 'ComplexDependency':
        return ComplexDependency(dependency_container.get(SimpleDependency))


class BoundDependency(SimpleDependency):
    @staticmethod
    def create(dependency_container: DependencyContainer) -> 'SimpleDependency':
        SimpleDependency.amount_created += 1
        return BoundDependency(BOUND_VALUE)


class TestDependencyContainer:
    @pytest.fixture(scope='function')
    def dependency_container(self) -> DependencyContainer:
        return DependencyContainer()

    @pytest.fixture(scope='function', autouse=True)
    def zero_amount_created(self):
        SimpleDependency.amount_created = 0

    def test_get_created_dependency(self, dependency_container):
        assert dependency_container.get(SimpleDependency).value == CREATE_VALUE
        assert SimpleDependency.amount_created == 1

    def test_get_added_dependency(self, dependency_container):
        dependency_container.add_dependency(SimpleDependency(ADD_VALUE))
        assert dependency_container.get(SimpleDependency).value == ADD_VALUE
        assert SimpleDependency.amount_created == 0

    def test_get_created_complex_dependency(self, dependency_container):
        assert dependency_container.get(ComplexDependency).dependency.value == CREATE_VALUE
        assert SimpleDependency.amount_created == 1

    def test_get_complex_dependency_with_added_dependency(self, dependency_container):
        dependency_container.add_dependency(SimpleDependency(ADD_VALUE))
        assert dependency_container.get(ComplexDependency).dependency.value == ADD_VALUE
        assert SimpleDependency.amount_created == 0

    def test_dependency_only_created_once(self, dependency_container):
        dependency_container.get(SimpleDependency)
        dependency_container.get(SimpleDependency)
        assert SimpleDependency.amount_created == 1

    def test_provided_dependency(self, dependency_container):
        dependency_container.add_provider(SimpleDependency, SimpleDependency.provide)
        assert dependency_container.get(SimpleDependency).value == PROVIDE_VALUE
        assert SimpleDependency.amount_created == 1

    def test_provided_dependency_only_created_once(self, dependency_container):
        dependency_container.add_provider(SimpleDependency, SimpleDependency.provide)
        dependency_container.get(SimpleDependency)
        dependency_container.get(SimpleDependency)
        assert SimpleDependency.amount_created == 1

    def test_dependency_only_created_twice_when_creating_explicitly(self, dependency_container):
        dependency_container.create(SimpleDependency)
        dependency_container.create(SimpleDependency)
        assert SimpleDependency.amount_created == 2

    def test_bound_dependency(self, dependency_container):
        dependency_container.bind(SimpleDependency, BoundDependency)
        assert dependency_container.get(SimpleDependency).value == BOUND_VALUE
        assert SimpleDependency.amount_created == 1
