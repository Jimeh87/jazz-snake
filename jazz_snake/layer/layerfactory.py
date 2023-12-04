from jazz_snake.board.stepdata import PointType
from jazz_snake.layer.boundarylayer import BoundaryLayer
from jazz_snake.layer.directpathlayer import DirectPathLayer
from jazz_snake.layer.goallayer import GoalLayer
from jazz_snake.layer.hazardlayer import HazardLayer
from jazz_snake.layer.lowriskzoneslayer import LowRiskZonesLayer
from jazz_snake.layer.path.availableareapathlayer import AvailableAreaPathLayer
from jazz_snake.layer.path.foodpathscorer import FoodPathScorer
from jazz_snake.layer.path.headattackpathscorer import HeadAttackPathScorer
from jazz_snake.layer.path.middlepathscorer import MiddlePathScorer
from jazz_snake.layer.path.pathslayer import PathsLayer
from jazz_snake.layer.path.tailpathscorer import TailPathScorer
from jazz_snake.layer.snakelayer import SnakeLayer
from jazz_snake.layer.snakelistenerlayer import SnakeListenerLayer
from jazz_snake.layer.stepsfrompointlayer import StepsFromPointLayer
from jazz_snake.layer.yourheadlayer import YourHeadLayer


class LayerFactory:

    def __init__(self, game_data):
        self._game_data = game_data

    def create_goal_layer(self) -> GoalLayer:
        return GoalLayer(self._game_data)

    def create_snake_listener_layer(self) -> SnakeListenerLayer:
        return SnakeListenerLayer(self._game_data['board']['snakes'])

    def create_snake_layer(self) -> [SnakeLayer]:
        layers = []
        for snake in self._game_data['board']['snakes']:
            layers.append(SnakeLayer(snake, self._game_data['you']))

        return layers

    def create_direct_path_layer(self) -> [DirectPathLayer]:
        layers = []
        for food in self._game_data['board']['food']:
            layers.append(DirectPathLayer(self._game_data['you']['head'], food))

        return layers

    def create_boundary_layer(self) -> BoundaryLayer:
        return BoundaryLayer()

    def create_low_risk_zones_layer(self) -> LowRiskZonesLayer:
        return LowRiskZonesLayer()

    def create_available_area_path_layer(self) -> AvailableAreaPathLayer:
        return AvailableAreaPathLayer(self._game_data['you'])

    def create_steps_from_point_layer(self) -> [StepsFromPointLayer]:
        layers = []

        # for i in range(len(self._game_data['board']['food'])):
        #     layers.append(StepsFromPointLayer(self._game_data['board']['food'][i], PointType.FOOD, 'food-' + str(i)))

        for snake in self._game_data['board']['snakes']:
            layers.append(StepsFromPointLayer(snake['head'], PointType.SNAKE_HEAD, snake['id']))

        layers.append(StepsFromPointLayer(self._game_data['you']['body'][-1],
                                          PointType.SNAKE_TAIL,
                                          'tail-' + self._game_data['you']['id']))

        return layers

    def create_your_head_layer(self) -> YourHeadLayer:
        return YourHeadLayer(self._game_data['you'])

    def create_paths_layer(self) -> PathsLayer:
        return PathsLayer(self._game_data['you'], [FoodPathScorer, TailPathScorer, MiddlePathScorer, HeadAttackPathScorer])

    def create_hazard_layer(self) -> HazardLayer:
        return HazardLayer(self._game_data['game']['ruleset']['settings'], self._game_data['board']['hazards'], self._game_data['you'])
