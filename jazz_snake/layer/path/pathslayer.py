from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.layer.path.pathfollower import PathFollower
from jazz_snake.layer.path.pathscorer import PathScorer


class PathsLayer:
    LIFE_CYCLE = LayerLifeCycle.PATHING

    def __init__(self, you_snake, path_scorers: [PathScorer]):
        self._you = you_snake
        self._path_scorers = path_scorers

    def visit(self, game_board: GameBoard):
        head_point = (self._you['head']['x'], self._you['head']['y'])
        points_with_directions = game_board.get_neighbour_cell_points_with_direction(head_point)

        paths = []
        for point_with_direction in points_with_directions:
            direction = point_with_direction['direction']
            start_point = point_with_direction['point']

            for step in game_board.get_cell(start_point[0], start_point[1], CellDataType.STEPS):
                for path_scorer in self._path_scorers:

                    if path_scorer.can_score_path(step):
                        path_follower = PathFollower(game_board,
                                                     step['point_type'],
                                                     step['point_id'],
                                                     step['distance'],
                                                     self._you['id'],
                                                     path_scorer)
                        paths.append(path_follower.score_path(direction, start_point))

                # if possible_path['point_type'] == PointType.SNAKE_HEAD:
                #     # TODO: At some point this would be a good snake killing path
                #     pass
                # elif possible_path['point_type'] == PointType.SNAKE_TAIL:
                #     pass

        game_board.add_paths(paths)
