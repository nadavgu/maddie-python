from dataclasses import dataclass

import pytest

from maddie.dependency import Dependency
from maddie.dependency_container import DependencyContainer

CREATE_VALUE = 1000
ADD_VALUE = 2000


@dataclass
class SimpleDependency(Dependency):
    value: int

    amount_created = 0

    @staticmethod
    def create(dependency_container: DependencyContainer) -> 'SimpleDependency':
        SimpleDependency.amount_created += 1
        return SimpleDependency(value=CREATE_VALUE)


@dataclass
class ComplexDependency(Dependency):
    dependency: SimpleDependency

    @staticmethod
    def create(dependency_container: DependencyContainer) -> 'ComplexDependency':
        return ComplexDependency(dependency_container.get(SimpleDependency))


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

