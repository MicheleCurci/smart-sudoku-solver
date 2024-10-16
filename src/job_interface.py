from abc import ABC, abstractmethod
from typing import TypeVar

A = TypeVar("A")


class AbstractJob(ABC):
    @abstractmethod
    def run(self, input: A) -> A:
        pass
