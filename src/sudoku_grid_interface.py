from abc import ABC, abstractmethod


class CellsBoxInterface(ABC):

    @abstractmethod
    def is_valid(self) -> bool:
        pass


class CellInterface(ABC):
    @abstractmethod
    def get_value(self) -> int:
        pass

    @abstractmethod
    def set_value(value: int) -> None:
        pass

    # @abstractmethod
    # def is_value_set(self) -> bool:
    #     pass

    @abstractmethod
    def get_candidates(self) -> set():
        pass

    # @abstractmethod
    # def has_single_candidate(self) -> bool:
    #     pass

    # @abstractmethod
    # def add_candidate(self) -> None:
    #    pass

    # @abstractmethod
    # def remove_candidate(self) -> None:
    #    pass

    @abstractmethod
    def set_candidates(self, candidates: set()) -> None:
        pass


class SquareInterface(ABC):
    @abstractmethod
    # def get(self, row: int, col: int) -> CellInterface:
    #     pass
    @abstractmethod
    def is_valid(self) -> bool:
        pass


class SudokuGridInterface(ABC):
    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def is_filled(self) -> bool:
        pass

    # @abstractmethod
    # def get_row_ith(self, row: int) -> CellsBoxInterface:
    #     pass

    # @abstractmethod
    # def get_col_ith(self, col: int) -> CellsBoxInterface:
    #     pass

    @abstractmethod
    def get_cell(self, row: int, col: int) -> CellInterface:
        pass

    # @abstractmethod
    # def set_cell_value(self, row: int, col: int, value: int) -> None:
    #     pass

    # @abstractmethod
    # def add_cell_candidate(self, cell: CellInterface, candidate: int):
    #     pass

    # @abstractmethod
    # def remove_cell_candidate(self, cell: CellInterface, candidate: int):
    #     pass

    @abstractmethod
    def get_square(self, row: int, col: int) -> SquareInterface:
        pass

    @abstractmethod
    def show(self) -> None:
        pass

    @abstractmethod
    def decode(self) -> str:
        pass
