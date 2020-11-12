import os
import random

import cherrypy

from jazz_snake.availablemoveslayer import AvailableMovesLayer
from jazz_snake.boundarylayer import BoundaryLayer
from jazz_snake.directpathlayer import DirectPathLayer
from jazz_snake.foodlayer import FoodLayer
from jazz_snake.gameboard import GameBoard
from jazz_snake.snakelayer import SnakeLayer

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "Jim",
            "color": "#4169e1",
            "head": "beluga",
            "tail": "pixel",
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json
        print(f"DATA: {data}")

        board = GameBoard(data['board']['height'], data['board']['width'])
        board.accept_layer(BoundaryLayer())
        board.accept_layer(SnakeLayer(data['you']))
        print(f"dos head: {data['you']['head']}")
        print(f"dos food: {data['board']['food']}")
        board.accept_layer(FoodLayer(data['board']['food']))
        board.accept_layer(AvailableMovesLayer(data['you']))
        board.accept_layer(DirectPathLayer(data['you']['head'], data['board']['food'][0]))
        board.print()

        your_head = data['you']['head']
        possible_moves = sorted([
            {'move': 'up', 'cell_value': board.get_cell_above(your_head['x'], your_head['y'])},
            {'move': 'down', 'cell_value': board.get_cell_below(your_head['x'], your_head['y'])},
            {'move': 'left', 'cell_value': board.get_cell_left(your_head['x'], your_head['y'])},
            {'move': 'right', 'cell_value': board.get_cell_right(your_head['x'], your_head['y'])}
        ], key=lambda move: move['cell_value'])

        best_moves = []
        safest_value = possible_moves[0]['cell_value']
        for possible_move in possible_moves:
            if possible_move['cell_value'] == safest_value:
                best_moves.append(possible_move)

        best_move = random.choice(best_moves)
        print(f"MOVE: {best_move}")

        return {
            'move': best_move['move']
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json
        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")), }
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
