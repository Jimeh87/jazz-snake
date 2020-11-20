from jazz_snake.board.pointtype import PointType
from jazz_snake.layer.path.pathscorer import PathScorer


class FoodPathScorer(PathScorer):

    @staticmethod
    def calculate_final_score(distance, scores):
        return (sum(scores) / (distance + 1)) + (distance * 10)

    @staticmethod
    def can_score_path(step):
        return step['point_type'] == PointType.FOOD

    def score_path(self):
        score = 0

        score = score + (self.get_death_threat_level() * 100)

        if self.you_snake_health < 15:
            score = score - 500

        for step in self.get_steps():
            if step['point_id'] == self.path_step['point_id']:
                continue

            if step['point_type'] == PointType.FOOD:
                # alternative food on path
                score = score - 1
            elif step['point_type'] == PointType.SNAKE_HEAD:
                if step['point_id'] != self.you_snake_id:
                    other_snake_distance = step['distance']
                    if other_snake_distance < self.current_distance:
                        score = score + 300
                    elif other_snake_distance == self.current_distance:
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
        return score * (1 + (1 / float(self.current_distance)))
