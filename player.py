class Player:
    def __init__(self, is_white: bool):
        self.is_white = is_white
        self.is_my_turn = is_white

    def can_play(self):
        return self.is_my_turn

    def turn(self):
        self.is_my_turn = not self.is_my_turn
