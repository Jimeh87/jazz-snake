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

    def test_should_go_for_food_2(self):
        with open('game_scenario_multi_snake.json') as file:
            data = file.read().replace('\n', '')

        game_data = json.loads(data)

        jazz_snake = JazzSnake(game_data)

        self.assertEqual("left", jazz_snake.calculate_move())

    def test_should_go_up_instead_of_down_into_food_with_no_exit(self):
        with open('game_scenario_doomed_food.json') as file:
            data = file.read().replace('\n', '')

        game_data = json.loads(data)

        jazz_snake = JazzSnake(game_data)

        self.assertEqual("up", jazz_snake.calculate_move())

    def test_should_go_down_to_tail(self):
        with open('game_scenario_down_to_tail.json') as file:
            data = file.read().replace('\n', '')

        game_data = json.loads(data)

        jazz_snake = JazzSnake(game_data)

        self.assertEqual("down", jazz_snake.calculate_move())

