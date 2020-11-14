from jazz_snake.layer.areaslayer import AreasLayer
from jazz_snake.layer.boundarylayer import BoundaryLayer
from jazz_snake.layer.directpathlayer import DirectPathLayer
from jazz_snake.layer.foodlayer import FoodLayer
from jazz_snake.layer.snakelayer import SnakeLayer


class LayerFactory:

    def __init__(self, game_data):
        self._game_data = game_data

    def create_food_layer(self) -> FoodLayer:
        return FoodLayer(self._game_data['board']['food'])

    def create_snake_layer(self) -> SnakeLayer:
        # TODO All of the snakes
        return SnakeLayer(self._game_data['you'], self._game_data['you'])

    def create_direct_path_layer(self) -> [DirectPathLayer]:
        layers = []
        for food in self._game_data['board']['food']:
            layers.append(DirectPathLayer(self._game_data['you']['head'], food))

        return layers

    def create_boundary_layer(self) -> BoundaryLayer:
        return BoundaryLayer()

    def create_areas_layer(self) -> AreasLayer:
        return AreasLayer(self._game_data['you'])
