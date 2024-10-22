from typing import Self


class Cell:
    def __init__(
        self,
        row: int,
        column: int,
        value: int,
        candidates: set[int] = set(range(1, 10)),
    ) -> None:
        self.row = row
        self.column = column
        self.candidates = candidates
        self.value = 0

        self.set_value(value)

    def __eq__(self, other: Self):
        return self.get_position() == other.get_position()

    def __repr__(self):
        return "(" + str(self.row) + ", " + str(self.column) + ")"

    def __hash__(self) -> int:
        return hash(str(self.row) + str(self.column) + str(self.candidates))

    def get_position(self) -> tuple:
        return (self.row, self.column)

    def get_value(self) -> int:
        return self.value

    def get_row(self) -> int:
        return self.row

    def get_col(self) -> int:
        return self.column

    def set_value(self, value: int) -> None:
        self.value = int(value)
        if self.value in range(1, 10):
            self.candidates = set()

    def is_marked(self) -> bool:
        return self.get_value() in range(1, 10)

    def is_valid(self) -> bool:
        return self.get_value() in range(10)

    def is_empty(self) -> bool:
        return self.get_value() == 0

    def get_candidates(self) -> set[int]:
        return self.candidates

    def set_candidates(self, candidates: set[int]) -> None:
        self.candidates = candidates

    def remove_candidate(self, candidate: int) -> None:
        self.candidates.discard(candidate)

    def remove_candidates(self, candidates: set[int]) -> None:
        self.candidates = self.candidates.difference(candidates)
