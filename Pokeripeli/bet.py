class Bethandler:
    def __init__(self):
        self.pot = 0
        self.bet_amount = 0
        self.earlier_bet = 0

    def bet(self, bet, current_bet):
        if not bet + current_bet >= self.earlier_bet:
            print("not enough bet")
            return 0
        else:
            self.pot += bet
            print("Pot is now", self.pot)
            print("earlier bet before turn was", self.earlier_bet)
            if current_bet + bet > self.bet_amount:
                self.bet_amount = current_bet + bet

            print("the guy who bet earlier bet was", current_bet)
            print(self.bet_amount, "amount of bet done")

            self.earlier_bet = bet + current_bet

            print("earlier bet after turn is", self.earlier_bet)
            return 1

    def everyone_same_bet(self, list_of_players_objects):
        same_bet = 0
        involved_in_round = 0
        earlier_player_bet = list_of_players_objects[0].bet
        print("Checking if everyone has bet same amount of money")
        for objec in list_of_players_objects:

            if objec.involved_in_the_round:
                if objec.all_in:
                    involved_in_round += 1
                    same_bet += 1
                else:
                    involved_in_round += 1
                    if objec.bet >= earlier_player_bet:
                        same_bet += 1

            earlier_player_bet = objec.bet

        print("Same amount of bets:", same_bet)
        print("Involved in round:", involved_in_round)

        if same_bet == involved_in_round:
            return True
        else:
            return False
