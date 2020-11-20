from enum import Enum, unique


@unique
class CellDataType(Enum):
    YOUR_HEAD = ('your_head', lambda values: values)
    DEATH_THREAT_LEVEL = ('death_threat', lambda values: max(values) if len(values) > 0 else 0)
    STEPS = ('steps', lambda values: values)
    GOAL = ('goal', lambda values: min(values) if len(values) > 0 else False)
    DESIRED_PATH = ('desired_path', lambda values: min(values) if len(values) > 0 else 255)

    def __init__(self, name, final_value_calc):
        self._name = name
        self._final_value_calc = final_value_calc

    def calculate_final_value(self, values):
        return self._final_value_calc(values)
