from dataclasses import dataclass
from enum import Enum, auto
from typing import List

from simulator import validators


class TileState(Enum):
    OCCUPIED = auto()
    FREE = auto()


@dataclass(frozen=True)
class Dimensions:
    rows: int
    columns: int


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


class Tile:
    def __init__(self, initial_state: TileState):
        self._state = initial_state

    @property
    def state(self) -> TileState:
        return self._state


class Board:
    def __init__(
            self,
            x_dim: int,
            y_dim: int
    ):
        self._board = dict()
        self._dimensions = Dimensions(
            rows=y_dim,
            columns=x_dim
        )

        self._initialise_board()

    def _initialise_board(self):
        for x in range(0, self._dimensions.columns):
            for y in range(0, self._dimensions.rows):
                coordinate = Coordinate(
                    x=x,
                    y=y
                )

                self._board[coordinate] = Tile(initial_state=TileState.FREE)

    @property
    def dimensions(self) -> Dimensions:
        return self._dimensions


    def _fetch_tiles_for_coordinate(self, coods: List[Coordinate]):
        return [self._board[cood] for cood in coods]

    def get_tiles_for_row(self, row_num: int) -> List[Tile]:
        validators.require_int_inclusive_range(row_num, 0, self._dimensions.rows, msg="Please follow board dimensions")

        coods = [Coordinate(x=col, y=row_num) for col in range(0, self._dimensions.columns)]

        return self._fetch_tiles_for_coordinate(coods)
