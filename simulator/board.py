from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional

from simulator import validators
from simulator.actors import Actor


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


@dataclass(frozen=True)
class ActorBundle:
    actor: Actor
    coordinate: Coordinate


class Tile:
    def __init__(self, actor: Optional[Actor] = None):
        self._actor = actor

    @property
    def state(self) -> TileState:
        return TileState.OCCUPIED if self._actor else TileState.FREE

    @property
    def actor(self) -> Actor:
        return self._actor

    @actor.setter
    def actor(self, actor: Optional[Actor]):
        self._actor = actor


class Board:
    def __init__(
            self,
            x_dim: int,
            y_dim: int,
            actor_bundles: List[ActorBundle] = None
    ):
        self._board = dict()
        self._dimensions = Dimensions(
            rows=y_dim,
            columns=x_dim
        )

        self._initialise_board()
        self._populate_actors(actor_bundles)

    def get_tiles_for_row(self, row_num: int) -> List[Tile]:
        validators.require_int_inclusive_range(row_num, 0, self._dimensions.rows, msg="Please follow board dimensions")

        coods = [Coordinate(x=col, y=row_num) for col in range(0, self._dimensions.columns)]

        return self._fetch_tiles_for_coordinates(coods)

    @property
    def dimensions(self) -> Dimensions:
        return self._dimensions

    def _initialise_board(self):
        for x in range(0, self._dimensions.columns):
            for y in range(0, self._dimensions.rows):
                coordinate = Coordinate(
                    x=x,
                    y=y
                )

                self._set_tile_for_coordinate(
                    tile=Tile(),
                    coordinate=coordinate
                )

    def _populate_actors(self, actor_bundles: List[ActorBundle]):
        for actor_bundle in actor_bundles:
            self._coordinate_within_bounds(actor_bundle.coordinate)
            
            tile = Tile(
                actor=actor_bundle.actor
            )

            self._set_tile_for_coordinate(
                tile=tile,
                coordinate=actor_bundle.coordinate
            )

    def _fetch_tiles_for_coordinates(self, coods: List[Coordinate]):
        return [self._board[cood] for cood in coods]

    def _fetch_all_tiles(self):
        coods = [
            Coordinate(x=col, y=row)
            for col in range(0, self._dimensions.columns)
            for row in range(0, self._dimensions.rows)
        ]

        return self._fetch_tiles_for_coordinates(coods)

    def _set_tile_for_coordinate(self, tile: Tile, coordinate: Coordinate):
        self._board[coordinate] = tile

    def _coordinate_within_bounds(self, coordinate: Coordinate):
        validators.require_int_inclusive_range(
            coordinate.x,
            0,
            self._dimensions.columns,
            msg="Actor coordinate exceeds number of columns"
        )

        validators.require_int_inclusive_range(
            coordinate.y,
            0,
            self._dimensions.rows,
            msg="Actor coordinate exceeds number of rows"
        )
