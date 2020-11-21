from jazz_snake.board.goaltype import GoalType
from jazz_snake.board.stepdata import PointType, StepData
from jazz_snake.layer.path.pathscorer import PathScorer


class FoodPathScorer(PathScorer):

    @staticmethod
    def calculate_final_score(distance, scores):
        return (sum(scores) / (distance + 1)) + (distance * 10)

    @staticmethod
    def can_score_path(step: StepData, goal_type: GoalType, you_snake_id):
        return goal_type == GoalType.FOOD and step.is_on_path(PointType.SNAKE_HEAD, you_snake_id)

    def score_path(self):
        score = 0

        score = score + (self.get_death_threat_level() * 100)

        for step in self.get_steps():
            if self.path_step.is_same_path(step):
                continue

            if step.point_type == PointType.SNAKE_HEAD:
                if not step.is_on_path(PointType.SNAKE_HEAD, self.you_snake_id):
                    other_snake_distance = step.distance
                    if other_snake_distance < self.path_step.distance:
                        score = score + 300
                    elif other_snake_distance == self.path_step.distance:
                        # TODO Should compare snake lengths
                        score = score + 300
                    else:
                        score = score - 1

        if self.has_your_tail_in_path():
            score = score - 100
        else:
            score = score + 500

        if score < 0:
            score = 1

        if self.you_snake_health < 15:
            score = score - 100
        return score * (1 + (1 / float(self.path_step.distance)))
