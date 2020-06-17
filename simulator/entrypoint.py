from simulator.board import Board
from simulator.visualiser import Visualiser


def main():
    board = Board(100, 10)
    visualiser = Visualiser()

    visualiser.print_snapshot(board)


if __name__ == "__main__":
    main()
