class Player:
    def __init__(self, starting_money):
        self.money = starting_money
        self.card_in_hand = [0, 0]
        self.bet = 0
        self.involved_in_the_round = True
        self.involved_in_the_game = True
        self.best_hand = {}
        self.all_in = False
