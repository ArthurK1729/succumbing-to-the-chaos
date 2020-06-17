from simulator.actors import RabbitActor
from simulator.board import Board, ActorBundle, Coordinate
from simulator.visualiser import Visualiser


def main():
    actor_bundles = [
        ActorBundle(
            actor=RabbitActor(),
            coordinate=Coordinate(
                x=5,
                y=5
            )
        )
    ]

    board = Board(
        x_dim=15,
        y_dim=10,
        actor_bundles=actor_bundles
    )

    visualiser = Visualiser()

    visualiser.print_snapshot(board)


if __name__ == "__main__":
    main()
