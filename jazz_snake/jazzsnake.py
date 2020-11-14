import random

from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard
from jazz_snake.layer.layerfactory import LayerFactory
from texttable import Texttable


class JazzSnake:

    def __init__(self, game_data):
        self._game_data = game_data
        layer_factory = LayerFactory(game_data)
        self._board = GameBoard(game_data['board']['height'], game_data['board']['width'])
        self._board.accept_layers(
            layer_factory.create_food_layer(),
            layer_factory.create_boundary_layer(),
            layer_factory.create_areas_layer(),
            layer_factory.create_snake_layer(),
            layer_factory.create_direct_path_layer()
        )

        # self._board.print()

    def calculate_move(self) -> str:
        your_head = self._game_data['you']['head']

        possible_moves = self._board.get_neighbour_final_cells(your_head['x'], your_head['y'])
        random.shuffle(possible_moves)
        possible_moves.sort(key=lambda m: (m['cell'][CellDataType.DEATH_THREAT_LEVEL],
                                           -int(m['cell'][CellDataType.AVAILABLE_AREA] * 1000),
                                           m['cell'][CellDataType.DESIRED_PATH]))

        JazzSnake.print_cells(possible_moves)

        print(f"MOVE: {possible_moves[0]['direction']}")

        return possible_moves[0]['direction']

    @staticmethod
    def print_cells(possible_moves):
        table = Texttable()
        table.set_max_width(400)
        table.set_deco(Texttable.BORDER | Texttable.HLINES | Texttable.VLINES)
        table.set_cols_align(['l' for _ in possible_moves])
        table.set_cols_valign(['t' for _ in possible_moves])

        row = []
        for possible_move in possible_moves:
            row.append(f"'direction': {possible_move['direction']} \n"
                       + f"'point': {possible_move['point']} \n"
                       + ("\n".join("{!r}: {!r},".format(k.name, v) for k, v in possible_move['cell'].items())))

        table.add_row(row)

        print(table.draw())
