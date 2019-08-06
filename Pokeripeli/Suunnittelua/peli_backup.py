# TIE-02100 Johdatus ohjelmointiin
# Teemu Helenius, teemu.helenius@tuni.fi, opiskelijanumero: 275152
# Pokeripeli: Perus texas hold'em no limit panostuksella. Muut pelaajat AI.
# säännöt: https://fi.wikipedia.org/wiki/Texas_hold_em

from tkinter import *
import random
from player import Player
from cards import Cardshandler
from bet import Bethandler

CARDPICS = []
BUTTONPICS = ["DEALER.gif", "SB.gif", "BB.gif"]
CARDS = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
NUMBER_OF_AI = 4
STARTING_MONEY = 200
# Small blind = 1,6% starting money
SB = STARTING_MONEY // 60
BB = SB * 2

# Padat
for I in CARDS:
    CARDPICS.append("P" + I + ".gif")
# Hertat
for I in CARDS:
    CARDPICS.append("H" + I + ".gif")
# Ristit
for I in CARDS:
    CARDPICS.append("RI" + I + ".gif")
# Ruudut
for I in CARDS:
    CARDPICS.append("RU" + I + ".gif")

# Pakka, 52. "kortti"
CARDPICS.append("pakka.gif")
# Kansi, 53. "kortti"
CARDPICS.append("kansi.gif")


class Game:

    def __init__(self):
        self.__window = Tk()
        self.__window.title("Texas Hold'em")

        # Järjestys pata, hertta, risti, ruutu, pakka ja viimeinen kortti kortin takapuoli
        self.__cardpics = []
        # Järjestys Dealer, BB, SB
        self.__buttonpics = []

        for picfile in CARDPICS:
            pic = PhotoImage(file=picfile)
            self.__cardpics.append(pic)

        for picfile in BUTTONPICS:
            pic = PhotoImage(file=picfile)
            self.__buttonpics.append(pic)

        # UI liittyvät asiat
        # Käsikorttien ärjestys (2 kpl) pelaaja 0 ja 1, ai1 2 ja 3, ai2 4 ja 5, ..
        self.__cardpic_in_hand_labels = []
        # Pöytäkorttien järjestys vasemmalta oikealle
        self.__cardpic_tablelabel = []
        self.__playeractionsbuttons = {}

        # Kaikkien listojen järjestys: pelaaja, ai1, ai2, ai3, ..
        self.__moneylabels = []
        self.__betlabels = []
        self.__blindlabels = []

        # Pelaamisen toimintoihin liittyvät asiat
        # Oliot, jotka hoitaa blindit, korttipakan ja panostuksen
        self.blindhandler = None
        # Luodaan korttipakan käsittelijä olio, joka pitää esim. lukua jäljellä olevista korteista
        self.__cardshandler = Cardshandler()
        # Luodaan panoksen käsittelijä olio, joka pitää huolta, että panostetaan oikea määrä
        self.bethandler = Bethandler()
        # Pelaaja ja ai oliot
        self.__player_and_ai_objects = []
        # Blindien paikat
        self.__dealer_pos = 0

        # Kokonaispotin label
        self.__potlabel = Label(self.__window)
        self.__potlabel.grid(row=4, column=0)

        # Ilmoitustekstit label
        self.__infotextlabel = Label(self.__window)
        self.__infotextlabel.grid(row=5, column=1, columnspan=2)
        self.__infotextlabel.configure(text="infoteksit, saattaa olla lause", wraplength=140,
                                       justify=LEFT)

        self.__raiseerrortextlabel = Label(self.__window)
        self.__raiseerrortextlabel.grid(row=5, column=7, columnspan=2)

        # Pöytäkorttien labelit
        for i in range(5):
            new_label = Label(self.__window)
            new_label.grid(row=4, column=i + 2)
            self.__cardpic_tablelabel.append(new_label)
            self.__cardpic_tablelabel[i].configure(
                image=self.__cardpics[53])

        # Pelaajan labelit (Kortit, rahat, blind, panos, toiminnot)

        # Kortit
        for i in range(2):
            new_label = Label(self.__window)
            new_label.grid(row=6, column=1 + i, rowspan=2)
            self.__cardpic_in_hand_labels.append(new_label)

        # Rahat
        self.__moneylabels.append(Label(self.__window))
        self.__moneylabels[0].grid(row=7, column=3)

        # Blindi
        self.__blindlabels.append(Label(self.__window))
        self.__blindlabels[0].grid(row=7, column=0)

        # Panos
        self.__betlabels.append(Label(self.__window))
        self.__betlabels[0].grid(row=7, column=4)

        # Toiminnot (Raise, Call, Fold, ALL-IN, Deal)

        # Raise Entry
        self.__raiseentry = Entry(self.__window, width=8, validate="key")
        self.__raiseentry.grid(row=6, column=7)
        # Määritellään validatecommand
        vcmd = (self.__raiseentry.register(self.raise_validate), '%P', '%d')
        self.__raiseentry.configure(validatecommand=vcmd)

        # Raise Button
        self.__playeractionsbuttons["raise"] = Button(self.__window)
        self.__playeractionsbuttons["raise"].grid(row=6, column=8)
        self.__playeractionsbuttons["raise"].configure(text="Raise", width=6, command=self.raise_)

        # Call
        self.__playeractionsbuttons["call"] = Button(self.__window)
        self.__playeractionsbuttons["call"].grid(row=6, column=9)
        self.__playeractionsbuttons["call"].configure(text="Call", width=6, command=self.call)

        # Fold
        self.__playeractionsbuttons["fold"] = Button(self.__window)
        self.__playeractionsbuttons["fold"].grid(row=7, column=8)
        self.__playeractionsbuttons["fold"].configure(text="Fold", width=6, command=self.fold)

        # ALL-IN
        self.__playeractionsbuttons["allin"] = Button(self.__window)
        self.__playeractionsbuttons["allin"].grid(row=7, column=9)
        self.__playeractionsbuttons["allin"].configure(text="ALL-IN", width=6, command=self.all_in)

        # Deal
        self.__playeractionsbuttons["deal"] = Button(self.__window)
        self.__playeractionsbuttons["deal"].grid(row=7, column=7)
        self.__playeractionsbuttons["deal"].configure(text="Deal", width=6, command=self.deal)

        # AI:den korttien, rahojen, blindin ja panostuksen labelit
        välit = 0
        for i in range(NUMBER_OF_AI):
            # Rahat
            new_label = Label(self.__window)
            new_label.grid(row=0, column=i + 1 + välit)
            self.__moneylabels.append(new_label)
            # Panostus
            new_label = Label(self.__window)
            new_label.grid(row=2, column=i + 1 + välit)
            self.__betlabels.append(new_label)
            # Blindit
            new_label = Label(self.__window)
            new_label.grid(row=2, column=i + välit)
            self.__blindlabels.append(new_label)
            # Kortit
            for j in range(2):
                new_label = Label(self.__window)
                new_label.grid(row=1, column=i + j + välit)
                self.__cardpic_in_hand_labels.append(new_label)
            välit += 2

        # Passiiviset labelit, ei attribuutteina

        # AI tekstit
        for i in range(NUMBER_OF_AI):
            Label(self.__window, text="AI " + str(i + 1)).grid(row=0, column=i * 3)

        # Pakka
        Label(self.__window, image=self.__cardpics[52]).grid(row=4, column=8)

        # Aloittaa pelin valmistelun
        self.init_game()

    def init_game(self):
        # Pelin config

        # Arvotaan dealerin paikka
        luku = random.randint(0, NUMBER_OF_AI)
        # Ja siitä seuraavat saavat SB ja BB

        # SB
        # Jos seuraava menee listan yli
        sb_pos = 0
        if luku + 1 > NUMBER_OF_AI:
            sb_pos = 0
        else:
            sb_pos = luku + 1

        # BB
        bb_pos = 0
        # Jos dealerista kaksi eteenpäin menee listan yli
        if luku + 2 > NUMBER_OF_AI:
            uusi_luku = luku + 2 - NUMBER_OF_AI - 1
            bb_pos = uusi_luku
        else:
            bb_pos = luku + 2

        # Luodaan blindin_käsittelijä olio ja kerrotaan sille aloitus SB, BB, luku = mistä dealer
        # aloitti sb ja bb paikka ja number of ai joka määrittää pelissä olevien positioiden määrän.
        self.blindhandler = Blindhandler(SB, BB, luku, sb_pos, bb_pos, NUMBER_OF_AI)

        # Luodaan pelaaja olio
        self.__player_and_ai_objects.append(Player(STARTING_MONEY))

        # Luodaan ai oliot halutulla aloitusrahalla ja kerrotaan niille blindhandler ja bethandler oliot
        for i in range(NUMBER_OF_AI):
            self.__player_and_ai_objects.append(AI(STARTING_MONEY, self.blindhandler, self.bethandler))

        # Pelin aloitus UI
        self.__potlabel.configure(text="Pot:\n0€")
        for i in range(NUMBER_OF_AI + 1):
            self.__betlabels[i].configure(text="Bet: 0€")
            self.__moneylabels[i].configure(text="200€")

        # Pöytäkortit
        for cardlabel in self.__cardpic_in_hand_labels:
            cardlabel.configure(image=self.__cardpics[53])

    def round_setup(self):
        # Blindit
        if self.game_continue():
            # Blindien paikat
            self.blindhandler.move_blinds()
            # Player in turn paikka
            # Maksetaan blindit, kerrotaan bethandlerille, että blindit on maksettu ja AI:lle kuinka
            # paljon on maksanut. Kerrotaan myös pelaaja oliolle. Bethandlerille kokonaispotti
            # SB
            self.__player_and_ai_objects[self.blindhandler.sb_pos].money -= self.blindhandler.sb
            self.__player_and_ai_objects[self.blindhandler.sb_pos].bet = self.blindhandler.sb

            # Edellinen bet pelin alussa on sb
            self.bethandler.earlier_bet = self.blindhandler.sb

            # BB
            self.__player_and_ai_objects[self.blindhandler.bb_pos].money -= self.blindhandler.bb
            self.__player_and_ai_objects[self.blindhandler.bb_pos].bet = self.blindhandler.bb

            # Viimeisin bet pelin alussa on bb
            self.bethandler.bet_amount = self.blindhandler.bb

            # Kokonais potti pelissä
            self.bethandler.pot = self.blindhandler.sb + self.blindhandler.bb

            # Jaetaan kortit
            for pelaaja in self.__player_and_ai_objects:
                for i in range(2):
                    pelaaja.card_in_hand[i] = self.__cardshandler.draw_a_card()

            # Käsikortit (Tyhjennetään vanhat ja lisätään uudet)
            for cardlabel in self.__cardpic_in_hand_labels:
                cardlabel.configure(image="")
                cardlabel.configure(image=self.__cardpics[53])

            # Pöytäkortit
            for cardlabel in self.__cardpic_tablelabel:
                cardlabel.configure(image="")
                cardlabel.configure(image=self.__cardpics[53])

            # Päivitetään UI
            self.update_ui()
        else:
            # TODO
            self.update_ui()
            self.__infotextlabel.configure(text="Game over")

    def deal(self):

        # Uusi kierros
        if self.__cardshandler.deal_counter == 0:
            print("Starting new round")
            self.round_setup()
            self.__playeractionsbuttons["deal"].configure(text="Change Turns", command=self.turn)

        # Flop
        if self.__cardshandler.deal_counter == 1:
            print("Time for flop")
            for i in range(3):
                card = self.__cardshandler.draw_a_card()
                self.__cardshandler.card_on_table.append(card)
                self.__cardpic_tablelabel[i].configure(image="")
                self.__cardpic_tablelabel[i].configure(image=self.__cardpics[card])
            self.__playeractionsbuttons["deal"].configure(text="Change Turns", command=self.turn)

            # Vuorossa oleva pelaaja on dealin jälkeen aina sb:stä alkaen pelissä
            # mukana oleva pelaaja
            self.blindhandler.player_in_turn = self.blindhandler.sb_pos
            for player in self.__player_and_ai_objects:
                if player.involved_in_the_round:
                    break
                else:
                    self.blindhandler.change_turn()

            if self.__player_and_ai_objects[0].involved_in_the_round:
                self.enable_player_buttons()

        # Turn
        if self.__cardshandler.deal_counter == 2:
            card = self.__cardshandler.draw_a_card()
            self.__cardshandler.card_on_table.append(card)

            self.__cardpic_tablelabel[3].configure(image="")
            self.__cardpic_tablelabel[3].configure(image=self.__cardpics[card])
            self.__playeractionsbuttons["deal"].configure(text="Change Turns", command=self.turn)

            # Vuorossa oleva pelaaja on dealin jälkeen aina sb:stä alkaen pelissä
            # mukana oleva pelaaja
            self.blindhandler.player_in_turn = self.blindhandler.sb_pos
            for player in self.__player_and_ai_objects:
                if player.involved_in_the_round:
                    break
                else:
                    self.blindhandler.change_turn()

            if self.__player_and_ai_objects[0].involved_in_the_round:
                self.enable_player_buttons()

        # River
        if self.__cardshandler.deal_counter == 3:
            card = self.__cardshandler.draw_a_card()
            self.__cardshandler.card_on_table.append(card)

            self.__cardpic_tablelabel[4].configure(image="")
            self.__cardpic_tablelabel[4].configure(image=self.__cardpics[card])
            self.__playeractionsbuttons["deal"].configure(text="Change Turns", command=self.turn)

            # Vuorossa oleva pelaaja on dealin jälkeen aina sb:stä alkaen pelissä
            # mukana oleva pelaaja
            self.blindhandler.player_in_turn = self.blindhandler.sb_pos
            for player in self.__player_and_ai_objects:
                if player.involved_in_the_round:
                    break
                else:
                    self.blindhandler.change_turn()

            if self.__player_and_ai_objects[0].involved_in_the_round:
                self.enable_player_buttons()

        self.__cardshandler.deal_counter += 1

    def turn(self):
        # Jos kaikkien vuoro on pelattu, ei voida pelata seuraavaa vuoroa ennen kuin tulee deal
        if self.blindhandler.turns_played >= NUMBER_OF_AI + 1 and self.bethandler.everyone_same_bet(
                self.__player_and_ai_objects):
            print("Waiting for next deal")
            if self.__cardshandler.deal_counter == 4:
                self.__playeractionsbuttons["deal"].configure(text="Check who won", command=self.round_winner)
                self.__cardshandler.deal_counter = -1
            else:
                self.__playeractionsbuttons["deal"].configure(text="Deal", command=self.deal)

            # Pelaaja ei voi korottaa tai tehdä muutakaan.
            self.__playeractionsbuttons["raise"].configure(state=DISABLED)
            self.__playeractionsbuttons["call"].configure(state=DISABLED)
            self.__playeractionsbuttons["fold"].configure(state=DISABLED)
            self.__playeractionsbuttons["allin"].configure(state=DISABLED)

            self.blindhandler.turns_played = 0
        # Muuten mennään vuoro kerrallaan myötäpäivään.
        else:
            # Jos on pelaajan vuoro ja pelaaja on vielä mukana kierroksella
            if self.blindhandler.player_in_turn == 0 and self.__player_and_ai_objects[0].involved_in_the_round:
                print("Player's turn")
                # Pelaaja ei voi vaihtaa vuoroansa pois ennen kuin on pelannut vuoron.
                self.__playeractionsbuttons["deal"].configure(state=DISABLED)

                self.enable_player_buttons()

                self.__infotextlabel.configure(text="It's your turn!")

            # AI:n vuoro jos ei ole pelaajan vuoro, jos AI ei ole mukana, seuraava vuoro
            elif self.__player_and_ai_objects[self.blindhandler.player_in_turn].involved_in_the_round:
                print("AI's turn")

                if self.__player_and_ai_objects[0].involved_in_the_round:
                    self.enable_player_buttons()

                self.__infotextlabel.configure(text="")
                self.__player_and_ai_objects[self.blindhandler.player_in_turn].turn()
                self.blindhandler.change_turn()
                self.update_ui()

            else:
                print("Player or AI" + str(self.blindhandler.player_in_turn) + "is not involved in round")
                self.blindhandler.change_turn()
                self.update_ui()

    def call(self):
        # Poistetaan call nappi käytöstä, jos pelaaja yrittää panostaa muulla kuin omalla vuorolla
        if self.blindhandler.player_in_turn != 0:
            self.__playeractionsbuttons["call"].configure(state=DISABLED)
            self.__infotextlabel.configure(text="It's not your turn.")

        else:
            print("Player calls")
            # Pelaajan call, maksaa omiin panoksiin nähden edellisen panoksen verran
            bet = self.bethandler.bet_amount - self.__player_and_ai_objects[0].bet
            print("Player bets", bet)
            self.__player_and_ai_objects[0].money -= bet
            # Kerrotaan bet handlerille betistä
            self.bethandler.bet(bet, self.__player_and_ai_objects[0].bet)
            self.__player_and_ai_objects[0].bet += bet
            print("Player current bet is now", self.__player_and_ai_objects[0].bet)
            self.blindhandler.change_turn()
            self.update_ui()

            # Palautetaan turn nappi käyttöön
            self.__playeractionsbuttons["deal"].configure(state=NORMAL)

    def raise_(self):
        # Poistetaan raise nappi käytöstä, jos pelaaja yrittää korottaa muulla kuin omalla vuorolla
        if self.blindhandler.player_in_turn != 0:
            self.__playeractionsbuttons["raise"].configure(state=DISABLED)
            self.__infotextlabel.configure(text="It's not your turn.")
            self.__raiseentry.delete(0, END)
        elif self.__raiseentry.get() == "":
            self.__raiseerrortextlabel.configure(text="Please type the amount of raise!", bg="red")
        else:
            print("Player raises")
            # Pelaaja korottaa, korotus tässä tapauksessa tarkoittaa korotusta edelliseen panostukseen
            # vaikka pelaaja ei olisi vielä maksanut panosta. Eli pelaaja maksaa panoksen JA korottaa
            # halutun summan verran. Ns. Check raise ei ole mahdollista

            earlier_bet = self.bethandler.earlier_bet
            raise_amount = int(self.__raiseentry.get()) + earlier_bet - self.__player_and_ai_objects[0].bet
            if raise_amount > self.__player_and_ai_objects[0].money:
                self.__raiseerrortextlabel.configure(text="You can't raise more than you have money!",
                                                     bg="red")
            else:
                print("Player bets", raise_amount)
                self.__player_and_ai_objects[0].money -= raise_amount
                # Kerrotaan bet handlerille betistä
                self.bethandler.bet(raise_amount, self.__player_and_ai_objects[0].bet)
                self.__player_and_ai_objects[0].bet += raise_amount
                print("Player current bet is now", self.__player_and_ai_objects[0].bet)
                self.blindhandler.change_turn()
                self.update_ui()

                # Palautetaan turn nappi käyttöön
                self.__playeractionsbuttons["deal"].configure(state=NORMAL)
                # Tyhjennetään Entry kenttä
                self.__raiseentry.delete(0, END)

    def all_in(self):
        # Poistetaan all in nappi käytöstä, jos pelaaja yrittää panostaa muulla kuin omalla vuorolla
        if self.blindhandler.player_in_turn != 0:
            self.__playeractionsbuttons["allin"].configure(state=DISABLED)
            self.__infotextlabel.configure(text="It's not your turn.")

        else:
            print("Player goes ALL-IN")
            # Pelaaja laittaa kaikki rahat peliin
            # Kerrotaan bet handlerille betistä
            self.bethandler.bet(self.__player_and_ai_objects[0].money, self.__player_and_ai_objects[0].bet)

            self.__player_and_ai_objects[0].bet += self.__player_and_ai_objects[0].money
            self.__player_and_ai_objects[0].money = 0

            print("Player current bet is now", self.__player_and_ai_objects[0].bet)
            self.blindhandler.change_turn()
            self.update_ui()

            # Palautetaan turn nappi käyttöön
            self.__playeractionsbuttons["deal"].configure(state=NORMAL)

    def fold(self):
        # Poistetaan all in nappi käytöstä, jos pelaaja yrittää foldaa muulla kuin omalla vuorolla
        if self.blindhandler.player_in_turn != 0:
            self.__playeractionsbuttons["fold"].configure(state=DISABLED)
            self.__infotextlabel.configure(text="It's not your turn.")

        else:
            print("Player folds")
            self.__player_and_ai_objects[0].involved_in_the_round = False
            self.blindhandler.change_turn()
            self.update_ui()

            # Palautetaan turn nappi käyttöön
            self.__playeractionsbuttons["deal"].configure(state=NORMAL)

            # Poistetaan pelaajan napit käytöstä.
            self.__playeractionsbuttons["call"].configure(state=DISABLED)
            self.__playeractionsbuttons["raise"].configure(state=DISABLED)
            self.__playeractionsbuttons["allin"].configure(state=DISABLED)
            self.__playeractionsbuttons["fold"].configure(state=DISABLED)

    def enable_player_buttons(self):
        self.__playeractionsbuttons["call"].configure(state=NORMAL)
        self.__playeractionsbuttons["raise"].configure(state=NORMAL)
        self.__playeractionsbuttons["allin"].configure(state=NORMAL)
        self.__playeractionsbuttons["fold"].configure(state=NORMAL)

    def game_continue(self):
        # Palauttaa True tai False, riipuen täyttyykö pelin jatkumisehdot

        # Voitto = kaikilla AI pelaajilla loppui rahat
        laskuri = 0
        for ai in self.__player_and_ai_objects[1:]:
            if ai.money <= 0:
                laskuri += 1
        if laskuri == NUMBER_OF_AI:
            print("All AI eliminated")
            return False
        # Rahat loppu
        if self.__player_and_ai_objects[0].money <= 0:
            print("Player got no money left")
            return False
        print("Game is allowed to continue")
        return True

    def round_winner(self):
        print("Checking who won the round")
        # Lista pelaaja/pelaajista jotka voitti tai olivat tasapelissä. tie= False tai True
        winner, tie = self.evaluate_cards()

        if tie:
            # Rahasumma mikä jaetaan = potti // voittajien määrällä
            shared_pot = self.bethandler.pot // len(winner)

            # Jaetaan rahat
            for player in winner:
                player.money += shared_pot
        else:
            # Voittaja saa potin rahat itselleen
            winner.money += self.bethandler.pot

        # Päivitetään UI, koska UI tyhjentää infotekstikentän, pitää infoteksti lisätä vasta UI:n
        # tyhjennyksen jälkeen
        self.update_ui()

        if tie:
            ties = []
            for player in winner:
                i = self.__player_and_ai_objects.index(player)
                if i == 0:
                    ties.append(" Player,")
                else:
                    ties.append(" " + str(i) + ",")

            self.__infotextlabel.configure(text="It's a tie between {}".format(ties))

        else:
            i = self.__player_and_ai_objects.index(winner)
            if i == 0:
                self.__infotextlabel.configure(text="You won!")
            else:
                self.__infotextlabel.configure(text="AI" + str(i) + " won!")

        # Resetataan asiat, mitkä pitää resettaa ennen uutta kierrosta
        # Cardshandleri
        self.__cardshandler.reset()
        # Pelaajien betit, mukana kierroksella ja paras käsi
        for player in self.__player_and_ai_objects:
            player.bet = 0
            player.involved_in_the_round = True
            player.best_hand = {}

        # Vaihdetaan nappi "New round", joka aloittaa uuden kierroksen
        self.__playeractionsbuttons["deal"].configure(text="New round",
                                                      command=self.deal)

    def evaluate_cards(self):
        print("Evaluating cards")
        for player in self.__player_and_ai_objects:
            if player.involved_in_the_round:
                seven_card_combo = []
                # Muodostetaan seitsemän kortin käsi
                for card in player.card_in_hand:
                    seven_card_combo.append(card)
                for card in self.__cardshandler.card_on_table:
                    seven_card_combo.append(card)
                print("Seven card combo per player", seven_card_combo)

                suited_list = self.__cardshandler.suited(seven_card_combo)

                # Lower straight, tarkoittaa että suora on 1-5, jossa yksi on ässä. Mutta koska ässä
                # aiheuttaisi ongelmia kahden suoran tarkastelussa (isompi voittaa), palauttaa
                # funktio straight tässä tapauksessä ässän numerolla 100. Ja koska biggest card funktio
                # etsii pienintä korttia, ei tämä ässä sotke enää isoimmman kortin vertailua, koska se
                # on joka tapauksessa pienin, ns 1. kortti jota ei pakasta normaalisti löydy.
                straight_list, lower_straight = self.__cardshandler.straight(seven_card_combo)

                same_of_a_kind, hand = self.__cardshandler.same_of_a_kind(seven_card_combo)
                full_house, hand_fullhouse = self.__cardshandler.same_of_a_kind(seven_card_combo, full_house=True)

                # Värisuora
                if len(suited_list) != 0 and len(straight_list) != 0:
                    straight_flush = []
                    # Tarkastellaan erityistapaus
                    if lower_straight:
                        # Koska straight palauttaa ässän numerolla 100, ei sitä löydy normaalista
                        # pakasta, ja näin ollen värisuoraa ei saada muodostettua normaalilla viidellä
                        # kortilla. Tässä tapauksessa riittää, että löytyy neljä korttia suorasta, jotka
                        # löytyvät myös väristä. Huom värissä, pitää olla tällöin ässä.

                        # Tarkastetaan, että väristä löytyy ässä.
                        if [x for x in [0, 13, 26, 39] if x in suited_list]:

                            for card in suited_list:
                                # Jos värin kortti on ässä, lisätään se käsin straight_flush listaan,
                                # koska sitä ei löydy suoran listasta(numerolla 100)
                                if card in [0, 13, 26, 29]:
                                    straight_flush.append(card)
                                if card in straight_list:
                                    straight_flush.append(card)

                                if len(straight_flush) >= 5:
                                    player.best_hand[8] = straight_flush
                                    print("Player got (lower) straight flush!")

                    else:
                        for card in suited_list:
                            if card in straight_list:
                                straight_flush.append(card)

                        if len(straight_flush) >= 5:
                            player.best_hand[8] = straight_flush
                            print("Player got straight flush!")

                # Neloset
                elif len(same_of_a_kind) != 0 and hand == 7:
                    print("Player got four of a kind!")
                    player.best_hand[7] = same_of_a_kind

                # Full House
                elif len(full_house) != 0 and hand_fullhouse == 6:
                    print("Player got full house!")
                    player.best_hand[6] = full_house

                # Väri
                elif len(suited_list) != 0:
                    print("Player got flush!")
                    player.best_hand[5] = suited_list

                # Suora
                elif len(straight_list) != 0:
                    if lower_straight:
                        print("Player got lower straight")
                    else:
                        print("Player got straight!")
                    player.best_hand[4] = straight_list

                # Kolmoset
                elif len(same_of_a_kind) != 0 and hand == 3:
                    print("Player got three of a kind!")
                    player.best_hand[3] = same_of_a_kind

                # Kaksi paria
                elif len(same_of_a_kind) != 0 and hand == 2:
                    print("Player got two pair!")
                    player.best_hand[2] = same_of_a_kind

                # Pari
                elif len(same_of_a_kind) != 0 and hand == 1:
                    print("Player got pairs!")
                    player.best_hand[1] = same_of_a_kind

                # Hai
                else:
                    print("Player got Highcard!")
                    player.best_hand[0] = self.__cardshandler.biggest_of_whats_left(seven_card_combo, [], 5)

            # Jos pelaaja ei ole mukana kierroksella
            else:
                continue

        # Etsitään voittavat kädet ja käsitellään tilanne jos niitä on useampia

        # Dicti, jossa key on pelaajan käden arvo ja value on pelaaja objecti
        player_hands_values = {}

        # Käydään läpi pelaajien käsien arvot ja pelaaja objectit ja lisätään ne dictiin
        print(self.__player_and_ai_objects)
        for player in self.__player_and_ai_objects:
            # Parhaan käden key:t = pelaajan käden arvo
            for key in player.best_hand.keys():
                if key in player_hands_values:
                    player_hands_values[key].append(player)
                else:
                    player_hands_values[key] = [player]

        print("Player hand values and objects", player_hands_values)

        # Järjestetään pelaajien kädet parhaimmasta huonoimpaan(isoimmasta pienimpään)
        player_hands_values = dict(sorted(player_hands_values.items(), reverse=True))

        print("Sorted player hands values", player_hands_values)
        # Voittava käsi, jossa key=käden arvo ja value=pelaaja objecti(t)
        winning_hands = {}
        # Voittavien käsien kortit lisätään omaan listaansa (Voittavien käsien järjestyksessä)
        list_of_winning_cards = []

        # Lista dictin key:stä (Käden arvoista)
        lista = list(player_hands_values.keys())
        # Aikaisempi käsi
        # Ensimmäisen pelaajan käden arvo = "aikaisempi käsi" = ensimmäinen voittava käsi
        earlier_hand = lista[0]
        print("(First hand)", earlier_hand)

        i = 0
        # Käydään läpi pelaajien kädet ja etsitään jos löytyy yhtä hyviä käsiä
        for hand_value in player_hands_values:
            print("Hand value", hand_value)
            if hand_value == earlier_hand:
                print("Same hand value")
                winning_hands[hand_value] = player_hands_values[hand_value]

                # Lisätään pelaajien kortit listaan
                for player in player_hands_values[hand_value]:
                    list_of_winning_cards.append(player.best_hand[hand_value])

            earlier_hand = hand_value
            i += 1

        # Jos voittavia käsiä on enemmän kuin yksi pitää tarkastella ne tapaukset erikseen sen
        # voittavan/voittavien käden perusteella.
        winning_hand_value = list(winning_hands.keys())[0]

        print("Voittavan käden arvo", winning_hand_value)
        i = 0
        if len(winning_hands[winning_hand_value]) > 1:
            # Voittavat pelaajat. Samassa järjestyksessä kuin voittavat kortit
            winning_players = []
            # Lisätään pelaajat listaan
            for lista in list(winning_hands.values()):
                for player in lista:
                    winning_players.append(player)

            print("Voittavat pelaajat", winning_players)

            # Helpot tapaukset
            # Värisuora, suora
            if winning_hand_value in [8, 4]:
                player_who_won = winning_players[0]
                players_in_tie = []
                biggest_card = 50
                for player in winning_players:
                    print("Lista voittavista korteista", list_of_winning_cards[i])
                    player_biggest_card = self.__cardshandler.biggest_card(list_of_winning_cards[i])

                    if player_biggest_card < biggest_card:
                        player_who_won = player
                        players_in_tie = [player]

                        biggest_card = player_biggest_card
                        print("Biggest card is now", biggest_card)
                        i += 1

                    elif player_biggest_card == biggest_card:
                        players_in_tie.append(player)
                        i += 1

                if len(players_in_tie) > 1:
                    print("Tasapelissä", players_in_tie)
                    return players_in_tie, True

                print("Voittaja", player_who_won)
                return player_who_won, False

            # Kikkerit
            # Neloset, full house, väri, kolmoset, kaksi paria, pari ja hai
            if winning_hand_value in [7, 6, 5, 3, 2, 1, 0]:

                # Dict "pääkorteista"
                #   key = pelaaja   value=lista pääkorteista
                main_cards = {}

                # Dict kikkereistä, suuruusjärjestyksessä.
                #   key = pelaaja   value=lista kikkereistä
                kicker_cards = {}

                print("Lista voittavista korteista", list_of_winning_cards)
                # Kerätään dict pääkorteista
                # Hain ja värin tapauksessa kaikki ovat kikkereitä
                if winning_hand_value in [7, 6, 3, 2, 1]:
                    i = 0
                    # Täyskäden tapauksessa muodostetaan main lista kolmoslistasta ja parilistasta
                    if winning_hand_value == 6:
                        for player in winning_players:
                            # Uudelleen organisoidaan listaa hieman
                            list_of_cards = []
                            three_of_kind = list_of_winning_cards[i][0:3]
                            pair = list_of_winning_cards[i][3:5]
                            list_of_cards.append(three_of_kind)
                            list_of_cards.append(pair)
                            print("Täyskäsi", list_of_cards)
                            main_cards[player] = list_of_cards
                            i += 1

                    # Kaksi paria tarvii myös vähän uudelleen organisointia
                    elif winning_hand_value == 2:
                        for player in winning_players:
                            # Uudelleen organisoidaan listaa hieman
                            list_of_cards = []
                            first_pair = list_of_winning_cards[i][0][0:2]
                            second_pair = list_of_winning_cards[i][0][2:4]

                            # Järjestetään eka ja toka pari sen mukaan, kumpi on isompi
                            first_pair_value = self.__cardshandler.biggest_card(first_pair)
                            second_pair_value = self.__cardshandler.biggest_card(second_pair)
                            if second_pair_value < first_pair_value:
                                temporary = first_pair
                                first_pair = second_pair
                                second_pair = temporary

                            list_of_cards.append(first_pair)
                            list_of_cards.append(second_pair)
                            print("Kaksi paria", list_of_cards)
                            main_cards[player] = list_of_cards
                            i += 1

                    else:
                        for player in winning_players:
                            main_cards[player] = [list_of_winning_cards[i][0]]
                            i += 1

                i = 0
                # Kerätään dict kikkereistä
                # Täyskädessä kaikki on main kortteja
                if winning_hand_value != 6:
                    # Jos väri tai hai, kaikki kikkereitä
                    if winning_hand_value in [5, 0]:
                        for player in winning_players:
                            kicker_cards[player] = list_of_winning_cards[i]
                            i += 1
                    else:
                        for player in winning_players:
                            kicker_cards[player] = list_of_winning_cards[i][1]
                            i += 1

                print("Main cards", main_cards)
                print("Kickers", kicker_cards)

                # Käydään dict pääkorteista läpi ja etsitään jokaisen pelaajan pääkorteista suurin
                # Tarkistetaan onko yhtä suuria pääkortteja, jos on etsitään toiseksi suurin. Jos on
                # yhtäsuuria toiseksi suurimpia kortteja, etsitään kolmanneksi suurin jne.

                list_of_players_in_tie = []
                winner_player = None

                # Hain ja värin tapauksessa kaikki kortit ovat kikkereitä
                if winning_hand_value not in [5, 0]:

                    # Neloset, kolmoset ja pari riittää yksi kerta
                    if winning_hand_value in [7, 3, 1]:
                        loops = 1
                    # Täyskäsi ja kaksi paria kaksi kierrosta
                    else:
                        loops = 2

                    for i in range(loops):

                        list_of_players_in_tie.clear()
                        highest_card = 50

                        for player in main_cards:
                            current_card = self.__cardshandler.biggest_card(main_cards[player][i])

                            if current_card < highest_card:
                                highest_card = current_card
                                print("New highest card", highest_card)
                                winner_player = player

                            elif current_card == highest_card:
                                if len(list_of_players_in_tie) == 0:
                                    list_of_players_in_tie = [player]
                                    # Lisätään viimeksi voitolla ollut tasapelien joukkoon.
                                    list_of_players_in_tie.append(winner_player)
                                else:
                                    list_of_players_in_tie.append(player)
                                    print("Uusi tasapeli main korteissa", list_of_players_in_tie)

                        if winner_player not in list_of_players_in_tie:
                            print("Found winner", winner_player)
                            return winner_player, False

                # Jos pääkorttien jälkeen on vielä tasapeli TAI oli kyseessä hai TAI väri,
                # ruvetaan käymään läpi kikkereitä
                if len(list_of_players_in_tie) > 1 or winning_hand_value in [5, 0]:

                    # Täyskäden tapauksessa kaikki ovat main kortteja
                    if winning_hand_value != 6:

                        for i in range(len(kicker_cards[winning_players[0]])):
                            print("Kikker korttien listan pituus",
                                  len(kicker_cards[winning_players[0]]))
                            list_of_players_in_tie.clear()
                            highest_card = 50

                            # Tarkastellaan, ketkä on vielä tasapelissä ja niiden kikkereitä
                            for player in list_of_players_in_tie:

                                current_card = self.__cardshandler.biggest_card([kicker_cards[player][i]])

                                if current_card < highest_card:
                                    highest_card = current_card
                                    print("Uusi korkein kortti, kikkereiden joukosta", highest_card)
                                    winner_player = player

                                elif current_card == highest_card:
                                    if len(list_of_players_in_tie) == 0:
                                        list_of_players_in_tie = [player]
                                        # Lisätään viimeksi voitolla ollut tasapelien joukkoon
                                        list_of_players_in_tie.append(winner_player)
                                    else:
                                        list_of_players_in_tie.append(player)
                                    print("Uusi tasapeli kikkereiden joukossa",
                                          list_of_players_in_tie)

                            # Jos löydetään kierroksella voittaja
                            if winner_player not in list_of_players_in_tie:
                                print("Voittaja", winner_player)
                                return winner_player, False

                if len(list_of_players_in_tie) > 1:
                    print("Tasapeli", list_of_players_in_tie)
                    return list_of_players_in_tie, True

        print("Voittaja", winning_hands[winning_hand_value][0])
        return winning_hands[winning_hand_value][0], False

    def update_ui(self):
        # Tyhjennetään vanha ui

        # Infoteksti
        self.__infotextlabel.configure(text="")

        # Blindit
        for label in self.__blindlabels:
            label.configure(image="")

        # Rahat
        for label in self.__moneylabels:
            label.configure(text="")

        # Potti
        self.__potlabel.configure(text="")

        # Betit
        for betlabel in self.__betlabels:
            betlabel.configure(text="")

        # Lisätään uudet

        # Blindit
        self.__blindlabels[self.blindhandler.dealer_pos].configure(image=self.__buttonpics[0])
        self.__blindlabels[self.blindhandler.sb_pos].configure(image=self.__buttonpics[1])
        self.__blindlabels[self.blindhandler.bb_pos].configure(image=self.__buttonpics[2])

        laskuri = 0
        # Rahat
        for label in self.__moneylabels:
            money = self.__player_and_ai_objects[laskuri].money
            label.configure(text=str(money) + "€")
            laskuri += 1

        # Potti
        self.__potlabel.configure(text="Pot:\n" + str(self.bethandler.pot) + "€")

        # Betit
        laskuri = 0
        for betlabel in self.__betlabels:
            betlabel.configure(text="Bet: " + str(self.__player_and_ai_objects[laskuri].bet) + "€")
            laskuri += 1

        laskuri = 0
        number = 0
        # Kortit TEST
        for cardlabel in self.__cardpic_in_hand_labels:

            cardnumber = self.__player_and_ai_objects[laskuri].card_in_hand[number]

            cardlabel.configure(image=self.__cardpics[cardnumber])

            if number == 0:
                number = 1
            else:
                number = 0
                laskuri += 1

    def start(self):
        self.__window.mainloop()

    def raise_validate(self, syöte, toimenpide):
        if toimenpide == "1":
            if not syöte.isdigit():
                self.__window.bell()
                self.__raiseerrortextlabel.configure(text="Please enter integral.", bg="red")
                return False
        self.__raiseerrortextlabel.configure(text="", bg='SystemButtonFace')
        return True


class Blindhandler:
    def __init__(self, sb, bb, dealer_starting_pos, sb_pos, bb_pos, player_positions):
        self.sb = sb
        self.bb = bb
        self.dealer_pos = dealer_starting_pos
        self.sb_pos = sb_pos
        self.bb_pos = bb_pos
        self.positions = player_positions
        # SB aloittaa aina vuoron, kun uusi kierros alkaa
        self.player_in_turn = sb_pos
        # Number of turns played per round
        self.turns_played = 0

    def change_blind_size(self):
        self.sb = self.sb * 2
        self.bb = self.sb * 2
        print("Changed blind sizes")
        print("SB", self.sb)
        print("BB", self.bb)

    def move_blinds(self):
        print("Moving blinds")
        # Positiot samat kun pelissä (pelaaja = 0, ai1, ai2, ..)

        # dealerin paikka yksi eteenpäin
        if self.dealer_pos + 1 > self.positions:
            self.dealer_pos = 0
        else:
            self.dealer_pos += 1

        # sb paikka yksi eteenpäin
        if self.sb_pos + 1 > self.positions:
            self.sb_pos = 0
        else:
            self.sb_pos += 1

        # bb paikka yksi eteenpäin
        if self.bb_pos + 1 > self.positions:
            self.bb_pos = 0
        else:
            self.bb_pos += 1

        # Päivitetään kuka on vuorossa
        self.player_in_turn = self.sb_pos

        print("Player in turn", self.player_in_turn)
        print("Turns played", self.turns_played)

    def change_turn(self):

        if self.player_in_turn + 1 > self.positions:
            self.player_in_turn = 0
            self.turns_played += 1
            print("Turn changed to", self.player_in_turn)
            print("Turns played", self.turns_played)

        else:
            self.player_in_turn += 1
            self.turns_played += 1
            print("Turn changed to", self.player_in_turn)
            print("Turns played", self.turns_played)


class AI:

    def __init__(self, starting_money, blindhandler_objec, bethandler_objec):
        self.money = starting_money
        self.card_in_hand = [0, 0]
        self.bet = 0
        self.blindhandler = blindhandler_objec
        self.bethandler = bethandler_objec
        self.involved_in_the_round = True
        self.best_hand = {}

    def turn(self):
        print("AI turn activated")
        bet_amount = self.bethandler.bet_amount - self.bet
        print("AI earlier bet was", self.bet)
        print("AI bets", bet_amount)
        self.money -= bet_amount
        self.bethandler.bet(bet_amount, self.bet)
        self.bet += bet_amount
        print("AI earlier bet is now", self.bet)


def main():
    ui = Game()
    ui.start()


main()
