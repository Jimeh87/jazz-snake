from jazz_snake.board.goaltype import GoalType
from jazz_snake.board.stepdata import StepData, PointType
from jazz_snake.layer.path.pathscorer import PathScorer


class MiddlePathScorer(PathScorer):

    @staticmethod
    def calculate_final_score(distance, scores):
        return max(scores) if distance > 2 else 15000

    @staticmethod
    def can_score_path(step: StepData, goal_type: GoalType, you_snake_id):
        return goal_type == GoalType.CENTER and step.is_on_path(PointType.SNAKE_HEAD, you_snake_id)

    def score_path(self):
        score = 80

        score = score + (self.get_death_threat_level() * 100)

        for step in self.get_steps():
            if self.path_step.is_same_path(step):
                continue
            elif step.point_type == PointType.SNAKE_HEAD:
                if step.point_id != self.you_snake_id:
                    other_snake_distance = step.distance
                    if other_snake_distance < self.path_step.distance:
                        score = score + 10
                    elif other_snake_distance == self.path_step.distance:
                        score = score + 5
                    else:
                        score = score - 1

        if score < 0:
            score = 1

        return score