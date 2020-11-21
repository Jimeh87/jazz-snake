from jazz_snake.board.gameboarddata import GameBoardData, GameBoardDataAggregate


class SimpleData(GameBoardData):

    def __init__(self, simple_data):
        self.simple_data = simple_data


class SimpleDataAggregate(GameBoardDataAggregate):

    def __init__(self):
        self.simple_data = []

    def add_data(self, data: GameBoardData):
        self.simple_data.append(data)

    def to_string(self) -> str:
        return ", ".join("{}".format(d) for d in self.simple_data)
