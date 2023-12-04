from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.deaththreatdata import DeathThreatData, DeathThreatLevel
from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.layerlifecycle import LayerLifeCycle


class HazardLayer:

    LIFE_CYCLE = LayerLifeCycle.DEATH_THREAT_ANALYSIS

    def __init__(self, settings, hazards, you):
        self._settings = settings
        self._hazards = hazards
        self._you = you

    def visit(self, game_board: GameBoard):
        hazard_damage_per_turn = self._settings['hazardDamagePerTurn']
        health = self._you['health']

        if hazard_damage_per_turn is None or hazard_damage_per_turn == 0:
            return

        death_threat_level = DeathThreatLevel.SMALL
        if (health / hazard_damage_per_turn) <= 1:
            death_threat_level = DeathThreatLevel.SUICIDE
        elif (health / hazard_damage_per_turn) <= 2:
            death_threat_level = DeathThreatLevel.EXTREME
        elif (health / hazard_damage_per_turn) <= 7:
            death_threat_level = DeathThreatLevel.MEDIUM

        for cell in self._hazards:
            game_board.set_cell((cell['x'], cell['y']), CellDataType.DEATH_THREAT_LEVEL, DeathThreatData(death_threat_level))
