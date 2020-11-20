import json
import unittest

from jazz_snake.jazzsnake import JazzSnake


class TestJazzSnake(unittest.TestCase):

    def test_only_bad_options(self):
        with open('game_scenario.json') as file:
            data = file.read().replace('\n', '')

        game_data = json.loads(data)

        jazz_snake = JazzSnake(game_data)

        self.assertEqual("right", jazz_snake.calculate_move())

    def test_should_follow_tail(self):
        with open('game_scenario_follow_tail.json') as file:
            data = file.read().replace('\n', '')

        game_data = json.loads(data)

        jazz_snake = JazzSnake(game_data)

        self.assertEqual("right", jazz_snake.calculate_move())

