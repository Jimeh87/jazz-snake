from texttable import Texttable

from jazz_snake.board.gameboard import GameBoard, RelativePoint
from jazz_snake.layer.layerfactory import LayerFactory


class JazzSnake:

    def __init__(self, game_data):
        self._game_data = game_data
        self._point_direction_lookup = RelativePoint.get_point_direction_lookup((game_data['you']['head']['x'],
                                                                                 game_data['you']['head']['y']))
        layer_factory = LayerFactory(game_data)
        self._board = GameBoard(game_data['board']['height'], game_data['board']['width'])
        self._board.accept_layers(
            layer_factory.create_your_head_layer(),
            layer_factory.create_snake_listener_layer(),
            layer_factory.create_goal_layer(),
            layer_factory.create_boundary_layer(),
            layer_factory.create_low_risk_zones_layer(),
            layer_factory.create_available_area_path_layer(),
            layer_factory.create_steps_from_point_layer(),
            layer_factory.create_snake_layer(),
            # layer_factory.create_direct_path_layer(),
            layer_factory.create_paths_layer()
        )

        # self._board.print()

    def calculate_move(self) -> str:

        paths = self._board.get_paths()
        if not paths:
            print("No paths!!! :(")
            return "up"

        self.print_paths(paths)
        best_direction = self._point_direction_lookup[paths[0]['points'][0]]

        print(f"MOVE: {best_direction}")
        return best_direction

    def print_paths(self, paths):
        table = Texttable()
        table.set_max_width(400)
        table.set_cols_align(['l' for _ in range(8)])
        table.set_cols_valign(['t' for _ in range(8)])

        table.header(['direction', 'goal', 'point_type', 'point_id', 'distance', 'points', 'scores', 'final_score'])
        for path in paths:
            table.add_row([
                self._point_direction_lookup[path['points'][0]],
                path['goal_type'],
                path['point_type'],
                path['point_id'],
                path['distance'],
                '\n'.join(map(str, path['points'])),
                '\n'.join(map(str, path['scores'])),
                path['final_score']
            ])

        print(table.draw())
