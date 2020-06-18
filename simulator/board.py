import random
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional

from simulator import validators
from simulator.actors import Actor, TileSummary, Environment, FieldOfVision, Action


# random.seed = 42


class TileState(Enum):
    RABBIT_ACTOR = auto()
    FREE = auto()


@dataclass(frozen=True)
class Dimensions:
    rows: int
    columns: int


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    @property
    def up(self):
        return Coordinate(
            x=self.x,
            y=self.y - 1
        )

    @property
    def down(self):
        return Coordinate(
            x=self.x,
            y=self.y + 1
        )

    @property
    def left(self):
        return Coordinate(
            x=self.x - 1,
            y=self.y
        )

    @property
    def right(self):
        return Coordinate(
            x=self.x + 1,
            y=self.y
        )


@dataclass(frozen=True)
class ActorBundle:
    actor: Actor
    coordinate: Coordinate


class Tile:
    def __init__(self, actor: Optional[Actor] = None):
        self._actor = actor

    @property
    def is_actor_present(self) -> bool:
        return self._actor is not None

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
        self._populate_tiles_with_actors(actor_bundles)

    @property
    def dimensions(self) -> Dimensions:
        return self._dimensions

    def get_tiles_for_row(self, row_num: int) -> List[Tile]:
        validators.require_int_inclusive_range(row_num, 0, self._dimensions.rows, msg="Please follow board dimensions")

        coods = [Coordinate(x=col, y=row_num) for col in range(0, self._dimensions.columns)]

        return self._fetch_tiles_for_coordinates(coods)

    def progress_time(self):
        actor_bundles = self._fetch_actor_bundles()
        actor_bundle = random.choice(actor_bundles)

        cood = actor_bundle.coordinate
        actor = actor_bundle.actor

        up_tile = self._fetch_tile_for_coordinate(cood.up)
        down_tile = self._fetch_tile_for_coordinate(cood.down)
        left_tile = self._fetch_tile_for_coordinate(cood.left)
        right_tile = self._fetch_tile_for_coordinate(cood.right)

        env = Environment(
            FieldOfVision(
                up=TileSummary(is_passage_open=not up_tile.is_actor_present if up_tile else False),
                down=TileSummary(is_passage_open=not down_tile.is_actor_present if down_tile else False),
                left=TileSummary(is_passage_open=not left_tile.is_actor_present if left_tile else False),
                right=TileSummary(is_passage_open=not right_tile.is_actor_present if right_tile else False)
            )
        )

        action = actor.think(env)

        if action == Action.MOVE_UP:
            self._move_actor(actor_bundle, cood.up)
        elif action == Action.MOVE_DOWN:
            self._move_actor(actor_bundle, cood.down)
        elif action == Action.MOVE_LEFT:
            self._move_actor(actor_bundle, cood.left)
        elif action == Action.MOVE_RIGHT:
            self._move_actor(actor_bundle, cood.right)

    def _initialise_board(self):
        for x in range(0, self._dimensions.columns):
            for y in range(0, self._dimensions.rows):
                coordinate = Coordinate(
                    x=x,
                    y=y
                )
                self._reset_tile_for_coordinate(coordinate)

    def _populate_tiles_with_actors(self, actor_bundles: List[ActorBundle]):
        for actor_bundle in actor_bundles:
            self._coordinate_within_bounds(actor_bundle.coordinate)

            tile = Tile(
                actor=actor_bundle.actor
            )

            self._set_tile_for_coordinate(
                tile=tile,
                coordinate=actor_bundle.coordinate
            )

    def _move_actor(self, actor_bundle: ActorBundle, new_cood: Coordinate):
        self._reset_tile_for_coordinate(actor_bundle.coordinate)
        self._set_tile_for_coordinate(Tile(actor=actor_bundle.actor), new_cood)

    def _fetch_tile_for_coordinate(self, cood: Coordinate) -> Optional[Tile]:
        return self._fetch_tiles_for_coordinates([cood])[0]

    def _fetch_tiles_for_coordinates(self, coods: List[Coordinate]) -> List[Optional[Tile]]:
        return [(self._board[cood] if (cood in self._board) else None) for cood in coods]

    def _fetch_actor_bundles(self) -> List[ActorBundle]:
        coods = [
            Coordinate(x=col, y=row)
            for col in range(0, self._dimensions.columns)
            for row in range(0, self._dimensions.rows)
        ]

        actor_bundles = list()

        for cood in coods:
            if self._fetch_tile_for_coordinate(cood).is_actor_present:
                actor_bundles.append(
                    ActorBundle(
                        actor=self._fetch_tile_for_coordinate(cood).actor,
                        coordinate=cood
                    )
                )

        return actor_bundles

    def _set_tile_for_coordinate(self, tile: Tile, coordinate: Coordinate):
        self._board[coordinate] = tile

    def _reset_tile_for_coordinate(self, coordinate: Coordinate):
        self._board[coordinate] = Tile()

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
