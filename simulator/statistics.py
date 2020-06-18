import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from simulator.board import Board


class StatisticsSink(ABC):
    """
        Outputs the result of the computation
    """

    @abstractmethod
    def buffer(self, data: str):
        raise NotImplementedError

    @abstractmethod
    def flush(self):
        raise NotImplementedError


class ConsoleSink(StatisticsSink):
    def __init__(self):
        self._buffer = []

    def buffer(self, data: str):
        self._buffer.append(data)

    def flush(self):
        print("\n".join(self._buffer))
        self._clear_buffer()

    def _clear_buffer(self):
        self._buffer = []


class FileSink(StatisticsSink):
    def __init__(self, path: Path):
        self._buffer = []
        self._path = path
        self._buffer_capacity = 100

    def buffer(self, data: str):
        self._buffer.append(data)

        if self._is_flush_needed():
            self.flush()

    def _is_flush_needed(self):
        return len(self._buffer) >= self._buffer_capacity

    def flush(self):
        with self._path.open(mode="a") as f:
            for datum in self._buffer:
                f.write(datum)

        self._clear_buffer()

    def _clear_buffer(self):
        self._buffer = []


@dataclass(frozen=True)
class CentroidStatistic:
    x: float
    y: float
    tick: int

    @property
    def json(self) -> str:
        return json.dumps({"statistic": "centroid", "tick": self.tick, "x": self.x, "y": self.y})


@dataclass(frozen=True)
class ActorCountStatistic:
    count: int
    tick: int

    @property
    def json(self) -> str:
        return json.dumps({"statistic": "actor_count", "tick": self.tick, "count": self.count})


class StatisticsAggregator:
    def __init__(self, sink: StatisticsSink = ConsoleSink()):
        self._sink = sink

    def compute_actor_centroid(self, board: Board, tick: int):
        actor_bundles = board.actor_bundles

        statistic = CentroidStatistic(
            x=(sum([actor_bundle.coordinate.x for actor_bundle in actor_bundles]) / len(actor_bundles)),
            y=(sum([actor_bundle.coordinate.y for actor_bundle in actor_bundles]) / len(actor_bundles)),
            tick=tick
        )

        self._sink.buffer(data=statistic.json)

    def compute_actor_count(self, board: Board, tick: int):
        count = len(board.actor_bundles)

        statistic = ActorCountStatistic(
            count=count,
            tick=tick
        )

        self._sink.buffer(data=statistic.json)
