import random
from functools import reduce

from texttable import Texttable

from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.deaththreatdata import DeathThreatDataAggregate
from jazz_snake.board.gameboarddata import GameBoardDataAggregate, GameBoardData
from jazz_snake.board.stepdata import StepDataAggregate


class GameBoard:

    def __init__(self, height: int, width: int):
        self._height = height
        self._width = width
        self._board = GameBoard.create_board(height, width)
        self._paths = []
        self._goals = []

    @staticmethod
    def create_board(height, width):
        return [[GameBoard.create_cell() for _ in range(height + 2)] for _ in range(width + 2)]

    @staticmethod
    def create_cell():
        cell = {}
        for key in CellDataType:
            cell[key] = key.data_aggregate_type()

        return cell

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def _get_cell(self, point: ()) -> {}:
        return self._board[point[0]][point[1]]

    def get_cell_death_threat(self, point: ()) -> DeathThreatDataAggregate:
        return self._get_cell(point)[CellDataType.DEATH_THREAT_LEVEL]

    def get_cell_steps(self, point: ()) -> StepDataAggregate:
        return self._get_cell(point)[CellDataType.STEP]

    def get_cell(self, point: (), cell_data_type: CellDataType) -> GameBoardDataAggregate:
        return self._get_cell(point)[cell_data_type]

    def get_paths(self):
        # TODO This is a silly place to do this
        random.shuffle(self._paths)
        self._paths.sort(key=lambda p: p['final_score'])
        return self._paths

    def add_path(self, path: {}):
        self._paths.append(path)

    def add_paths(self, paths: []):
        self._paths.extend(paths)

    def add_goal(self, goal: {}):
        self._goals.append(goal)

    def get_goals(self):
        return self._goals

    def set_cell(self, point: (), cell_data_type: CellDataType, game_board_data: GameBoardData):
        self.get_cell(point, cell_data_type).add_data(game_board_data)

    def get_total_cells(self):
        return self._height * self._width

    def accept_layers(self, *layers):
        sorted_layers = []
        for layer in layers:
            if isinstance(layer, list):
                sorted_layers.extend(layer)
            else:
                sorted_layers.append(layer)
        sorted_layers.sort(key=lambda l: l.LIFE_CYCLE.value)

        for layer in sorted_layers:
            layer.visit(self)

    def print(self):
        height_range = reversed(range(-1, self.get_height() + 1))
        width_range = range(-1, self.get_width() + 1)

        table = Texttable()
        table.set_max_width(400)
        table.set_deco(Texttable.BORDER | Texttable.HLINES | Texttable.VLINES)
        table.set_cols_align(['l' for _ in width_range])
        table.set_cols_valign(['t' for _ in width_range])
        for y in height_range:
            row = []
            for x in width_range:
                cell = self._get_cell((x, y))
                row.append("'point': (" + str(x) + "," + str(y) + ")\n"
                           + ("\n".join("{!r}: {!r},".format(k.name, v.to_string()) for k, v in cell.items())))
            table.add_row(row)

        print(table.draw())


class RelativePoint:
    @staticmethod
    def up(point: ()):
        return point[0], point[1] + 1

    @staticmethod
    def down(point: ()):
        return point[0], point[1] - 1

    @staticmethod
    def left(point: ()):
        return point[0] - 1, point[1]

    @staticmethod
    def right(point: ()):
        return point[0] + 1, point[1]

    @staticmethod
    def get_neighbour_points(point: ()) -> [()]:
        return list(map(lambda d: d['point'], RelativePoint.get_neighbour_points_with_direction(point)))

    @staticmethod
    def get_neighbour_points_with_direction(point: ()) -> [dict]:
        return [
            {'direction': 'up', 'point': RelativePoint.up(point)},
            {'direction': 'down', 'point': RelativePoint.down(point)},
            {'direction': 'left', 'point': RelativePoint.left(point)},
            {'direction': 'right', 'point': RelativePoint.right(point)},
        ]

    @staticmethod
    def get_point_direction_lookup(point: ()) -> dict:
        return reduce(RelativePoint.reduce_to_dict, RelativePoint.get_neighbour_points_with_direction(point), {})

    @staticmethod
    def reduce_to_dict(current_value, next_value):
        current_value[next_value['point']] = next_value['direction']
        return current_value
