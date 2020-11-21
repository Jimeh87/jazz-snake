from jazz_snake.board.goaltype import GoalType
from jazz_snake.board.stepdata import PointType, StepData
from jazz_snake.layer.path.pathscorer import PathScorer


class TailPathScorer(PathScorer):

    @staticmethod
    def calculate_final_score(distance, scores):
        return max(scores)

    @staticmethod
    def can_score_path(step: StepData, goal_type: GoalType, you_snake_id):
        return goal_type == GoalType.TAIL and step.is_on_path(PointType.SNAKE_HEAD, you_snake_id)

    def score_path(self):
        score = 100

        score = score + (self.get_death_threat_level() * 100)

        for step in self.get_steps():
            if self.path_step.is_same_path(step):
                continue
            elif step.point_type == PointType.SNAKE_HEAD:
                if step.point_id != self.you_snake_id:
                    other_snake_distance = step.distance
                    if other_snake_distance < self.path_step.distance:
                        score = score + 50
                    elif other_snake_distance == self.path_step.distance:
                        score = score + 50
                    else:
                        score = score - 1

        if score < 0:
            score = 1
        return score * (1 + (1 / float(self.path_step.distance + 1)))
