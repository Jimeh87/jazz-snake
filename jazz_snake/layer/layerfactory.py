from jazz_snake.layer.areaslayer import AreasLayer
from jazz_snake.layer.boundarylayer import BoundaryLayer
from jazz_snake.layer.directpathlayer import DirectPathLayer
from jazz_snake.layer.foodlayer import FoodLayer
from jazz_snake.layer.lowriskzoneslayer import LowRiskZonesLayer
from jazz_snake.layer.snakelayer import SnakeLayer
from jazz_snake.layer.snakelistenerlayer import SnakeListenerLayer


class LayerFactory:

    def __init__(self, game_data):
        self._game_data = game_data

    def create_food_layer(self) -> FoodLayer:
        return FoodLayer(self._game_data['board']['food'])

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

    def create_areas_layer(self) -> AreasLayer:
        return AreasLayer(self._game_data['you'])
