from components.cards import Card, Color


class GameStatus(object):
    def __init__(self):
        self.red_points, self.blue_points = 0, 0

        # List of tuples of (red_card, blue_card)
        self.resolved_fights = []
        self.on_hold_fights = []

    @property
    def on_hold_points(self):
        two_pointers = [
            (red_card, blue_card) for red_card, blue_card in self.on_hold_fights
            if red_card == Card.ambassador and blue_card == Card.ambassador
        ]
        return len(self.on_hold_fights) + len(two_pointers)

    @property
    def winner(self):
        if self.red_points >= 4:
            return Color.red
        if self.blue_points >= 4:
            return Color.blue
        return None

    @property
    def all_fights(self):
        return self.resolved_fights + self.on_hold_fights

    @property
    def most_recent_fight(self):
        all_fights = self.all_fights
        return all_fights[-1] if all_fights else (None, None)

    @property
    def score_summary(self):
        player_scores = 'points: red {} to blue {}'\
            .format(self.red_points, self.blue_points)
        if self.on_hold_points:
            return player_scores + ' with {} points on hold'.format(self.on_hold_points)
        return player_scores
