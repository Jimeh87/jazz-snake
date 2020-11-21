from jazz_snake.board.gameboarddata import GameBoardData, GameBoardDataAggregate


class DeathThreatLevel:
    SAFE = 0
    SMALL = .1
    MEDIUM = 2
    HIGH = 3
    EXTREME = 4
    SUICIDE = 100


class DeathThreatData(GameBoardData):

    def __init__(self, death_threat_level: int, turns: int = None):
        self.level = death_threat_level
        self.turns = turns


class DeathThreatDataAggregate(GameBoardDataAggregate):

    def __init__(self):
        self.death_threat_data = []

    def add_data(self, data: GameBoardData):
        self.death_threat_data.append(data)

    def is_cell_safe(self, turn=None) -> bool:
        return self.get_death_threat_level(turn) < DeathThreatLevel.SUICIDE

    def get_death_threat_level(self, turn=None):
        highest_death_threat = DeathThreatLevel.SAFE
        for death_threat_datum in self.death_threat_data:
            if death_threat_datum.level > highest_death_threat \
                    and (turn is None or death_threat_datum.turns is None or death_threat_datum.turns >= turn):
                highest_death_threat = death_threat_datum.level

        return highest_death_threat

    def to_string(self) -> str:
        return str(self.get_death_threat_level()) + " - " + (", ".join("level[{}] turns[{}]".format(d.level, d.turns) for d in self.death_threat_data))
