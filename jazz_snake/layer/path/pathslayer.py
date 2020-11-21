from jazz_snake.board.gameboard import GameBoard, RelativePoint
from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.layer.path.pathfollower import PathFollower
from jazz_snake.layer.path.pathscorer import PathScorer


class PathsLayer:
    LIFE_CYCLE = LayerLifeCycle.PATHING

    def __init__(self, you_snake, path_scorers: [PathScorer]):
        self._you = you_snake
        self._path_scorers = path_scorers

    def visit(self, game_board: GameBoard):
        for goal in game_board.get_goals():
            for step in game_board.get_cell_steps(goal['point']).steps_data:
                for path_scorer in self._path_scorers:

                    if path_scorer.can_score_path(step, goal['type'], self._you['id']):
                        path_follower = PathFollower(game_board,
                                                     goal['type'],
                                                     step.point_type,
                                                     step.point_id,
                                                     step.distance,
                                                     self._you,
                                                     path_scorer)

                        path = path_follower.score_path(goal['point'])
                        if path['distance'] == 0:
                            print(f"Unexpected path distance of zero for {goal} and {path}")
                        else:
                            game_board.add_path(path_follower.score_path(goal['point']))
