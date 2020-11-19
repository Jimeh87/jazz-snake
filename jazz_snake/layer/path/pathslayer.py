from jazz_snake.board.PointType import PointType
from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.layer.path.foodpathscorer import FootPathScorer
from jazz_snake.layer.path.pathfollower import PathFollower
from jazz_snake.layer.path.pathscorer import PathScorer


class PathsLayer:
    LIFE_CYCLE = LayerLifeCycle.PATHING

    def __init__(self, you_snake):
        self._you = you_snake

    def visit(self, game_board: GameBoard):
        head_point = (self._you['head']['x'], self._you['head']['y'])
        points_with_directions = game_board.get_neighbour_cell_points_with_direction(head_point)

        paths = []
        for point_with_direction in points_with_directions:
            direction = point_with_direction['direction']
            start_point = point_with_direction['point']

            possible_paths = game_board.get_cell(start_point[0], start_point[1], CellDataType.STEPS)

            for possible_path in possible_paths:
                if possible_path['point_type'] == PointType.SNAKE_HEAD:
                    # TODO: At some point this would be a good snake killing path
                    pass
                elif possible_path['point_type'] == PointType.SNAKE_TAIL:
                    pass

                elif possible_path['point_type'] == PointType.FOOD:
                    path_follower = PathFollower(game_board,
                                                 possible_path['point_type'],
                                                 possible_path['point_id'],
                                                 possible_path['distance'],
                                                 self._you['id'],
                                                 FootPathScorer)
                    paths.append(path_follower.score_path(direction, start_point))

        game_board.add_paths(paths)
