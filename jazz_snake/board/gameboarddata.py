from abc import abstractmethod


class GameBoardData:
    pass


class GameBoardDataAggregate:

    @abstractmethod
    def add_data(self, data: GameBoardData):
        pass

    @abstractmethod
    def to_string(self) -> str:
        pass
