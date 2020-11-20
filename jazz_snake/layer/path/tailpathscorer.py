from jazz_snake.board.pointtype import PointType
from jazz_snake.layer.path.pathscorer import PathScorer


class TailPathScorer(PathScorer):

    @staticmethod
    def calculate_final_score(distance, scores):
        return max(scores)

    @staticmethod
    def can_score_path(step):
        return step['point_type'] == PointType.SNAKE_TAIL

    def score_path(self):
        score = 100

        score = score + (self.get_death_threat_level() * 100)

        for step in self.get_steps():
            if step['point_id'] == self.path_step['point_id']:
                continue
            elif step['point_type'] == PointType.SNAKE_HEAD:
                if step['point_id'] != self.you_snake_id:
                    other_snake_distance = step['distance']
                    if other_snake_distance < self.current_distance:
                        score = score + 10
                    elif other_snake_distance == self.current_distance:
                        score = score + 5
                    else:
                        score = score - 1

        if score < 0:
            score = 1
        return score * (1 + (1 / float(self.current_distance)))
