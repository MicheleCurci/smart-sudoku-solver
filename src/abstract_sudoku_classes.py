from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractCell(ABC):
    @abstractmethod
    def get_value(self) -> int:
        pass

    @abstractmethod
    def set_value(self, value: int) -> None:
        pass

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


class AbstractCellGroup(ABC):
    @abstractmethod
    def get_cells(self) -> set[AbstractCell]:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_candidates_union(self) -> set[int]:
        pass

    @abstractmethod
    def get_empty_cells(self) -> set[AbstractCell]:
        pass

    @abstractmethod
    def difference(self, other: AbstractCellGroup) -> AbstractCellGroup:
        pass


class AbstractSquare(ABC):
    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def flatten(self) -> set[AbstractCell]:
        pass

    @abstractmethod
    def get_rows(self) -> list[AbstractCellGroup]:
        pass

    @abstractmethod
    def get_columns(self) -> list[AbstractCellGroup]:
        pass

    @abstractmethod
    def get_empty_cells(self) -> set[AbstractCell]:
        pass

    @abstractmethod
    def get_other_empty_cells_in_square(
        self, main_cells: set[AbstractCell]
    ) -> AbstractCellGroup:
        pass


class AbstractGrid(ABC):
    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def is_filled(self) -> bool:
        pass

    @abstractmethod
    def get_cell(self, row: int, col: int) -> AbstractCell:
        pass

    @abstractmethod
    def get_rows(self) -> list[AbstractCellGroup]:
        pass

    @abstractmethod
    def get_columns(self) -> list[AbstractCellGroup]:
        pass

    @abstractmethod
    def set_cell_value(self, cell: AbstractCell, value: int) -> None:
        pass

    @abstractmethod
    def get_other_cells_on_row(self, row: int, col: int) -> AbstractCellGroup:
        pass

    @abstractmethod
    def get_other_cells_on_column(self, row: int, col: int) -> AbstractCellGroup:
        pass

    @abstractmethod
    def get_other_cells_in_grid(self, row: int, col: int) -> AbstractCellGroup:
        pass

    @abstractmethod
    def get_empty_cells_on_row(self, row: int) -> AbstractCellGroup:
        pass

    @abstractmethod
    def get_empty_cells_on_col(self, col: int) -> AbstractCellGroup:
        pass

    @abstractmethod
    def get_all_squares(self) -> list[AbstractSquare]:
        pass

    @abstractmethod
    def get_square(self, row: int, col: int) -> AbstractSquare:
        pass

    @abstractmethod
    def show(self) -> None:
        pass

    @abstractmethod
    def encode(self) -> str:
        pass
