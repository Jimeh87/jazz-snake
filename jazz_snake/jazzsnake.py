
from jazz_snake.board.gameboard import GameBoard
from jazz_snake.layer.layerfactory import LayerFactory
from texttable import Texttable


class JazzSnake:

    def __init__(self, game_data):
        self._game_data = game_data
        layer_factory = LayerFactory(game_data)
        self._board = GameBoard(game_data['board']['height'], game_data['board']['width'])
        self._board.accept_layers(
            layer_factory.create_your_head_layer(),
            layer_factory.create_snake_listener_layer(),
            layer_factory.create_food_layer(),
            layer_factory.create_boundary_layer(),
            layer_factory.create_low_risk_zones_layer(),
            layer_factory.create_available_area_path_layer(),
            layer_factory.create_steps_from_point_layer(),
            layer_factory.create_snake_layer(),
            layer_factory.create_direct_path_layer(),
            layer_factory.create_paths_layer()
        )

        # self._board.print()

    def calculate_move(self) -> str:
        paths = self._board.get_paths()
        if not paths:
            print("No paths!!! :(")
            return "up"

        self.print_paths(paths)
        best_path = paths[0]

        print(f"MOVE: {best_path['direction']}")
        return best_path['direction']

    @staticmethod
    def print_paths(paths):
        table = Texttable()
        table.set_max_width(400)
        table.set_cols_align(['l' for _ in range(7)])
        table.set_cols_valign(['t' for _ in range(7)])

        table.header(['direction', 'point_type', 'point_id', 'distance', 'points', 'scores', 'final_score'])
        for path in paths:
            table.add_row([
                path['direction'],
                path['point_type'],
                path['point_id'],
                path['distance'],
                '\n'.join(map(str, path['points'])),
                '\n'.join(map(str, path['scores'])),
                path['final_score']
            ])

        print(table.draw())

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
