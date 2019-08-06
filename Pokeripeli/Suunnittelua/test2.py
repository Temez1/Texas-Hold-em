class Test:
    def __init__(self, name, pelissä):
        self.name = name
        self.involved_in_the_game = pelissä

    def __str__(self):
        return str(self.name)

class Blindhandler:
    def __init__(self, sb, bb, dealer_starting_pos, sb_pos, bb_pos, player_positions):
        self.sb = sb
        self.bb = bb
        self.dealer_pos = dealer_starting_pos
        self.sb_pos = sb_pos
        self.bb_pos = bb_pos
        self.positions = player_positions
        # BB:stä seuraava aloittaa aina vuoron, kun uusi kierros alkaa
        try:
            self.player_in_turn = self.positions.index(player_positions[bb_pos + 1])
        except IndexError:
            self.player_in_turn = 0
        # Number of turns played per round
        self.turns_played = 0

    def change_blind_size(self):
        self.sb = self.sb * 2
        self.bb = self.sb * 2
        print("Changed blind sizes")
        print("SB", self.sb)
        print("BB", self.bb)

    def move_blinds(self):
        # TODO Korjaa kun pelaajat tippuu
        print("Moving blinds")

        # Dealer
        earlier = self.dealer_pos

        for i in range(len(self.positions)):
            if earlier + 1 == len(self.positions):
                earlier = -1

            next_player = self.positions[earlier + 1]

            if next_player.involved_in_the_game:
                self.dealer_pos = self.positions.index(next_player)
                break

            earlier += 1

        # SB
        earlier = self.dealer_pos

        for i in range(len(self.positions)):
            if earlier + 1 == len(self.positions):
                earlier = -1

            next_player = self.positions[earlier + 1]

            if next_player.involved_in_the_game:
                self.sb_pos = self.positions.index(next_player)
                break

            earlier += 1

        # BB
        earlier = self.dealer_pos

        for i in range(len(self.positions)):
            if earlier + 1 == len(self.positions):
                earlier = -1

            next_player = self.positions[earlier + 1]

            if next_player.involved_in_the_game:
                self.bb_pos = self.positions.index(next_player)
                break

            earlier += 1

        # Päivitetään kuka on seuraavana vuorossa
        earlier = self.bb_pos

        for i in range(len(self.positions)):
            if earlier + 1 == len(self.positions):
                earlier = -1

            next_player = self.positions[earlier + 1]

            if next_player.involved_in_the_game:
                self.player_in_turn = self.positions.index(next_player)
                break

            earlier += 1

        print("Turns played", self.turns_played)

    def change_turn(self):

        earlier = self.player_in_turn

        for i in range(len(self.positions)):
            if earlier + 1 == len(self.positions):
                earlier = -1

            next_player = self.positions[earlier + 1]

            if next_player.involved_in_the_game:
                self.player_in_turn = self.positions.index(next_player)
                break

            earlier += 1

        self.turns_played += 1

        print("Turn changed to", self.player_in_turn)
        print("Turns played", self.turns_played)


def main():
    testi = []
    for i in range(5):
        if i == 2:
            testi.append(Test(i, pelissä=False))
        else:
            testi.append(Test(i, pelissä=True))

    olio = Blindhandler(3, 6, 2, 3, 4, testi)
    print(testi)
    olio.move_blinds()

main()
