# class for game statistics
import json

class GameStats:
    # tracks statistics for user
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self._get_high_score()

        # start game in active state
        self.game_active = False

    def _get_high_score(self):
        # high score is never reset
        try:
            with open('highscore.json') as file :
                self.high_score = json.load(file)
        except FileNotFoundError :
            self.high_score = 0
            with open('highscore.json', 'w') as file :
                json.dump(self.high_score, file)
            return self.high_score
        else :
            return self.high_score

    def reset_stats(self):
        self.ships_left = self.settings.ships_available
        self.counter_aliens_shot = 0
        self.score = 0
        self.level = 1




