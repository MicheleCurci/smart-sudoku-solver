from abc import ABC, abstractmethod
from typing import TypeVar

A = TypeVar("A")  # the variable name must coincide with the string


class JobInterface(ABC):
    @abstractmethod
    def run(self, input: A) -> A:
        pass
