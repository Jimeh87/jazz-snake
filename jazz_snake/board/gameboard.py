import random

from texttable import Texttable

from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.deaththreatlevel import DeathThreatLevel


class GameBoard:

    def __init__(self, height: int, width: int):
        self._height = height
        self._width = width
        self._board = GameBoard.create_board(height, width)
        self._paths = []

    @staticmethod
    def create_board(height, width):
        return [[GameBoard.create_cell() for _ in range(height + 2)] for _ in range(width + 2)]

    @staticmethod
    def create_cell():
        cell = {}
        for key in CellDataType:
            cell[key] = []

        return cell

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def _get_cell(self, x, y=None) -> dict:
        if y is None:
            y = x[1]
            x = x[0]

        return self._board[x + 1][y + 1]

    def get_cell(self, x, y, cell_data_type: CellDataType) -> []:
        return self._get_cell(x, y)[cell_data_type]

    def get_calculated_cell(self, x, y, cell_data_type: CellDataType):
        return cell_data_type.calculate_final_value(self.get_cell(x, y, cell_data_type))

    def get_paths(self):
        # TODO This is a silly place to do this
        random.shuffle(self._paths)
        self._paths.sort(key=lambda p: p['final_score'])
        return self._paths

    def add_path(self, path: {}):
        self._paths.append(path)

    def add_paths(self, paths: []):
        self._paths.extend(paths)

    @staticmethod
    def get_neighbour_cell_points(x, y=None) -> [dict]:
        if y is None:
            y = x[1]
            x = x[0]

        return [
            RelativeCell.up(x, y),
            RelativeCell.down(x, y),
            RelativeCell.left(x, y),
            RelativeCell.right(x, y)
        ]

    @staticmethod
    def get_neighbour_cell_points_with_direction(x, y=None) -> [dict]:
        if y is None:
            y = x[1]
            x = x[0]

        return [
            {'direction': 'up', 'point': RelativeCell.up(x, y)},
            {'direction': 'down', 'point': RelativeCell.down(x, y)},
            {'direction': 'left', 'point': RelativeCell.left(x, y)},
            {'direction': 'right', 'point': RelativeCell.right(x, y)},
        ]

    def get_final_cell(self, x, y=None) -> dict:
        if y is None:
            y = x[1]
            x = x[0]
        final_cell = {}
        for key, value in self._get_cell(x, y).items():
            final_cell[key] = key.calculate_final_value(value)

        return final_cell

    def get_neighbour_final_cells(self, x, y) -> [dict]:
        neighbour_cell_points = self.get_neighbour_cell_points_with_direction(x, y)
        neighbour_final_cells = []
        for neighbour_cell_point in neighbour_cell_points:
            final_cell = self.get_final_cell(neighbour_cell_point['point'])
            neighbour_final_cells.append({**{'cell': final_cell}, **neighbour_cell_point})

        return neighbour_final_cells

    def get_relative_cell(self, x, y, cell_data_type: CellDataType, mapper):
        relative_cell = mapper(x, y)
        return self.get_cell(relative_cell[0], relative_cell[1], cell_data_type)

    def set_cell(self, x, y, cell_data_type: CellDataType, value):
        self._get_cell(x, y)[cell_data_type].append(value)

    def is_cell_safe(self, x, y):
        return self.get_final_cell(x, y)[CellDataType.DEATH_THREAT_LEVEL] <= DeathThreatLevel.SMALL

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
                cell = self._get_cell(x, y)
                row.append("'POINT': (" + str(x) + "," + str(y) + ")\n"
                           + ("\n".join("{!r}: {!r},".format(k.name, v) for k, v in cell.items())))
            table.add_row(row)

        print(table.draw())


class RelativeCell:
    @staticmethod
    def up(x, y):
        return x, y + 1

    @staticmethod
    def down(x, y):
        return x, y - 1

    @staticmethod
    def left(x, y):
        return x - 1, y

    @staticmethod
    def right(x, y):
        return x + 1, y
