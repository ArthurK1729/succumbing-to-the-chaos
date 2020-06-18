from typing import Tuple

from simulator.board import Board


class StatisticsAggregator:
    @staticmethod
    def compute_actor_centroid(board: Board) -> Tuple[float, float]:
        actor_bundles = board.actor_bundles

        x_mean = sum([actor_bundle.coordinate.x for actor_bundle in actor_bundles]) / len(actor_bundles)
        y_mean = sum([actor_bundle.coordinate.y for actor_bundle in actor_bundles]) / len(actor_bundles)

        return x_mean, y_mean
