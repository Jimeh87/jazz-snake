from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.deaththreatlevel import DeathThreatLevel
from jazz_snake.board.gameboard import GameBoard


class BoundaryLayer:

    LIFE_CYCLE = LayerLifeCycle.DEATH_THREAT_ANALYSIS

    def visit(self, game_board: GameBoard):
        min_width = -1
        max_width = game_board.get_width()
        min_height = -1
        max_height = game_board.get_height()
        for x in range(min_width, max_width + 1):
            for y in range(min_height, max_height + 1):
                death_threat_level = DeathThreatLevel.SAFE
                if x in (min_width, max_width) or y in (min_height, max_height):
                    death_threat_level = DeathThreatLevel.SUICIDE
                game_board.set_cell(x, y, CellDataType.DEATH_THREAT_LEVEL, death_threat_level)
