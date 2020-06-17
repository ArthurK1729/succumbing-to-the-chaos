from typing import List

from simulator.board import Board, TileState, Tile

_TILE_MAPPER = {
    TileState.FREE: " "
}


class Visualiser:
    def print_snapshot(self, board: Board):
        dimensions = board.dimensions

        self._print_top_border(dimensions.columns)

        for row_num in range(0, dimensions.rows):
            self._print_tile_row(board.get_tiles_for_row(row_num=row_num))

        self._print_bottom_border(dimensions.columns)

    def _print_tile_row(self, tiles: List[Tile]):
        mapped_tiles = [self._map_tile(tile) for tile in tiles]

        row = ["║"]
        row.extend(mapped_tiles)
        row.append("║")

        print("".join(row))

    def _print_top_border(self, columns: int):
        border = list()

        border.append("╔")
        border.extend("═" * columns)
        border.append("╗")

        print("".join(border))

    def _print_bottom_border(self, columns: int):
        border = list()

        border.append("╚")
        border.extend("═" * columns)
        border.append("╝")

        print("".join(border))

    def _map_tile(self, tile: Tile):
        return _TILE_MAPPER[tile.state]
