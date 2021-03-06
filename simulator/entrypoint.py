import time
from pathlib import Path

from simulator.actors import RabbitActor
from simulator.board import Board, ActorBundle, Coordinate
from simulator.statistics import StatisticsAggregator, FileSink
from simulator.visualiser import ConsoleVisualiser


def main():
    actor_bundles = [
        ActorBundle(
            actor=RabbitActor(),
            coordinate=Coordinate(
                x=n,
                y=n
            )
        ) for n in range(0, 20)
    ]

    board = Board(
        x_dim=200,
        y_dim=20,
        actor_bundles=actor_bundles
    )

    visualiser = ConsoleVisualiser()

    statistics_aggregator = StatisticsAggregator(FileSink(Path("statistics.log")))

    for tick in range(0, 1000):
        visualiser.print_snapshot(board)
        time.sleep(0.0001)
        board.progress_time()

        statistics_aggregator.compute_actor_centroid(board, tick)
        statistics_aggregator.compute_actor_count(board, tick)
        statistics_aggregator.compute_rabbit_count(board, tick)


if __name__ == "__main__":
    main()
