import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


@dataclass(frozen=True)
class TileSummary:
    is_wall: bool


@dataclass(frozen=True)
class FieldOfVision:
    up: Optional[TileSummary]
    down: Optional[TileSummary]
    left: Optional[TileSummary]
    right: Optional[TileSummary]


@dataclass(frozen=True)
class Environment:
    field_of_vision: FieldOfVision


class Action(Enum):
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()


class Actor(ABC):
    @abstractmethod
    def think(self, env: Environment) -> Action:
        raise NotImplementedError


class RabbitActor(Actor):

    def think(self, env: Environment) -> Action:
        directions = env.field_of_vision
        open_directions = [direction for direction in directions if direction is not None]

        chosen_direction = random.choice(open_directions)
