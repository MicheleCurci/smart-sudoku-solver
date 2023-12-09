from __future__ import annotations
from abc import ABC, abstractmethod

class CellInterface(ABC):

    @abstractmethod
    def get_value(self) -> int:
        pass

    @abstractmethod
    def set_value(self, value: int) -> None:
        pass

    # @abstractmethod
    # def is_value_set(self) -> bool:
    #     pass

    @abstractmethod
    def get_candidates(self) -> set[int]:
        pass

    @abstractmethod
    def set_candidates(self, candidates: set[int]) -> None:
        pass

    @abstractmethod
    def get_row(self) -> int:
        pass

    @abstractmethod
    def get_col(self) -> int:
        pass

    # @abstractmethod
    # def has_single_candidate(self) -> bool:
    #     pass

    # @abstractmethod
    # def add_candidate(self) -> None:
    #    pass

    @abstractmethod
    def remove_candidates(self, candidates_to_remove: set[int]) -> None:
       pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def is_marked(self) -> bool:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def get_position(self) -> tuple[int, int]:
        pass

class CellGroupInterface(ABC):

    @abstractmethod
    def get_cells(self) -> set[CellInterface]:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_candidates_union(self) -> set[int]:
        pass

    @abstractmethod
    def get_empty_cells(self) -> set[CellInterface]:
        pass

    @abstractmethod
    def difference(self, other: CellGroupInterface) -> CellGroupInterface:
        pass
    

class SquareInterface(ABC):
    #@abstractmethod
    # def get(self, row: int, col: int) -> CellInterface:
    #     pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def flatten(self) -> set[CellInterface]:
        pass

    @abstractmethod
    def get_rows(self) -> list[CellGroupInterface]:
        pass

    @abstractmethod
    def get_columns(self) -> list[CellGroupInterface]:
        pass

    @abstractmethod
    def get_empty_cells(self) -> set[CellInterface]:
        pass

    @abstractmethod
    def get_other_empty_cells_in_square(self, main_cells: set[CellInterface]) -> CellGroupInterface:
        pass

class GridInterface(ABC):
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
    # def get_row_ith(self, row: int) -> CellGroupInterface:
    #     pass

    # @abstractmethod
    # def get_col_ith(self, col: int) -> CellGroupInterface:
    #     pass

    @abstractmethod
    def get_cell(self, row: int, col: int) -> CellInterface:
        pass

    @abstractmethod
    def get_rows(self) -> list[CellGroupInterface]:
        pass

    @abstractmethod
    def get_columns(self) -> list[CellGroupInterface]:
        pass

    @abstractmethod
    def set_cell_value(self, cell: CellInterface, value: int) -> None:
        pass

    @abstractmethod
    def get_other_cells_on_row(self, row: int, col: int) -> CellGroupInterface:
        pass

    @abstractmethod
    def get_other_cells_on_column(self, row: int, col: int) -> CellGroupInterface:
        pass

    @abstractmethod
    def get_other_cells_in_grid(self, row: int, col: int) -> CellGroupInterface:
        pass

    @abstractmethod
    def get_empty_cells_on_row(self, row: int) -> CellGroupInterface:
        pass
    
    @abstractmethod
    def get_empty_cells_on_col(self, col: int) -> CellGroupInterface:
        pass

    # @abstractmethod
    # def add_cell_candidate(self, cell: CellInterface, candidate: int):
    #     pass

    # @abstractmethod
    # def remove_cell_candidate(self, cell: CellInterface, candidate: int):
    #     pass

    @abstractmethod
    def get_all_squares(self) -> list[SquareInterface]:
        pass

    @abstractmethod
    def get_square(self, row: int, col: int) -> SquareInterface:
        pass

    @abstractmethod
    def show(self) -> None:
        pass

    @abstractmethod
    def decode(self) -> str:
        pass
