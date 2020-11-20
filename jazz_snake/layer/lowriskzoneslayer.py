from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.deaththreatlevel import DeathThreatLevel
from jazz_snake.board.gameboard import GameBoard


class LowRiskZonesLayer:

    LIFE_CYCLE = LayerLifeCycle.DEATH_THREAT_ANALYSIS

    def visit(self, game_board: GameBoard):
        min_width = 0
        max_width = game_board.get_width()
        min_height = 0
        max_height = game_board.get_height()
        for x in range(min_width, max_width):
            for y in range(min_height, max_height):
                if x in (min_width, max_width - 1) or y in (min_height, max_height - 1):
                    game_board.set_cell(x, y, CellDataType.DEATH_THREAT_LEVEL, DeathThreatLevel.SMALL)
