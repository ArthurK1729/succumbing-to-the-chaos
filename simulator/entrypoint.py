import time

from simulator.actors import RabbitActor
from simulator.board import Board, ActorBundle, Coordinate
from simulator.statistics import StatisticsAggregator
from simulator.visualiser import Visualiser


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

    visualiser = Visualiser()

    for _ in range(0, 1000):
        visualiser.print_snapshot(board)
        time.sleep(0.0001)
        board.progress_time()
        print(StatisticsAggregator.compute_actor_centroid(board))


if __name__ == "__main__":
    main()
