import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


@dataclass(frozen=True)
class TileSummary:
    is_passage_open: bool


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
    DO_NOTHING = auto()


class Actor(ABC):
    @abstractmethod
    def think(self, env: Environment) -> Action:
        raise NotImplementedError


class RabbitActor(Actor):
    def think(self, env: Environment) -> Action:
        directions = env.field_of_vision
        possible_actions = []

        if up := directions.up:
            if up.is_passage_open:
                possible_actions.append(Action.MOVE_UP)

        if down := directions.down:
            if down.is_passage_open:
                possible_actions.append(Action.MOVE_DOWN)

        if left := directions.left:
            if left.is_passage_open:
                possible_actions.append(Action.MOVE_LEFT)

        if right := directions.right:
            if right.is_passage_open:
                possible_actions.append(Action.MOVE_RIGHT)

        if possible_actions:
            chosen_action = random.choice(possible_actions)
        else:
            chosen_action = Action.DO_NOTHING

        return chosen_action
