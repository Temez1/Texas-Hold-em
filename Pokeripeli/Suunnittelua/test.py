class Testi:
    def __init__(self):
        self.best_hand = {}
        self.biggest_card = 0


class Cards:
    def suited(self, cards_list):
        spades = []
        hearts = []
        clovers = []
        diamonds = []

        print("Testing if cards suited")

        for card in cards_list:
            new_pack = []
            for i in range(52):
                new_pack.append(i)
            # Katotaan mitä väriä kukin kortti on
            print("Current card is", card)
            if card in new_pack[0:13]:
                print("spade")
                spades.append(card)
            elif card in new_pack[13:26]:
                print("Heart")
                hearts.append(card)
            elif card in new_pack[26:39]:
                print("Clover")
                clovers.append(card)
            else:
                diamonds.append(card)
                print("Diamond")

        print("Amount of s,h,c,d =", len(spades), len(hearts), len(clovers), len(diamonds))
        print("Cards  of s,h,c,d =", spades, hearts, clovers, diamonds)

        if len(spades) >= 5:
            print("Was suited")
            return spades
        elif len(hearts) >= 5:
            print("Was suited")
            return hearts
        elif len(clovers) >= 5:
            print("Was suited")
            return clovers
        elif len(diamonds) >= 5:
            print("Was suited")
            return diamonds
        else:
            print("Wasn't suited")
            return []

    def biggest_card(self, cards_list):
        print("Finding biggest card")
        biggest_card = 100

        for card in cards_list:
            # Muutetaan isoimman kortin lukuarvo välille 0-12
            # HUOM ISOIN KORTTI ON 0 ELI ÄSSÄ, KURKO = 1, jne.
            if card > 38:
                card -= 39
            elif card > 25:
                card -= 26
            elif card > 12:
                card -= 13

            if card < biggest_card:
                biggest_card = card

        print("Biggest card was", biggest_card)
        return biggest_card

    def straight(self, cards_list):
        print("Testing if cards in straight")

        # Dict, jossa key= kortin arvo 0-13 ja value= kortin numero 0-51
        card_values_and_numbers = {}

        # Lisätään kortit dictiin
        for card in cards_list:
            # Jos ässä, lisätään se 13. kortiksi ns. "1", koska ässä voi olla suorassa numero "1"
            if card in [0, 13, 26, 39]:
                card_values_and_numbers[13] = card
            card_value = self.biggest_card([card])
            card_values_and_numbers[card_value] = card

        print("Kortit", card_values_and_numbers)
        # Järjestetään dict korttien arvojen mukaiseen järjestykseen (0-12)
        card_values_and_numbers = dict(sorted(card_values_and_numbers.items()))
        print("Sorted kortit", card_values_and_numbers)

        # Lista järjestetyistä korttien arvoista (0-13)
        list_of_card_values = list(card_values_and_numbers.keys())
        print("Lista korttien arvoista", list_of_card_values)
        # Lista järjestetyistä korttie numeroista
        list_of_card_numbers = list(card_values_and_numbers.values())
        print("Lista korttien numeroista", list_of_card_numbers)

        straight = []
        earlier_card = list_of_card_values[0] - 1

        for card in list_of_card_values:
            print("Kortti listasta", card)
            if (card - 1) == earlier_card:
                # Jos edellinen kortti on 2 pitää ottaa huomioon, että ässä jatkaa suoraa
                if earlier_card == 12:
                    print("Aiempi kortti oli 2")
                    straight.append(card_values_and_numbers[card])

                    if len(straight) == 5:
                        # Ässä on tässä tapauksessa numero 100, ettei se sekoita isointa
                        # korttia kun vertaillaan muita korttilistoja
                        lista = [100]
                        # Neljä viimeisintä korttia
                        lista.extend(list_of_card_numbers[-5:-1])

                        return lista, True

                # Jos edellinen kortti ei ollut 2 niin voidaan lisätä kortti
                else:
                    print("Listan pituus ennen lisäystä", len(straight))
                    straight.append(card_values_and_numbers[card])
                    earlier_card = card

                    print("Listan pituus lisäyksen jälkeen", len(straight))
                    if len(straight) == 5:
                        return straight, False
            else:
                straight.clear()
                straight.append(card_values_and_numbers[card])
                earlier_card = card

        # Palautetaan tyhjä lista merkiksi siitä, ettei löytynyt suoraa (Ja ihan sama True/False)
        print("Didn't find straight")
        return [], False

    def same_of_a_kind(self, cards_list, full_house=False, two_pairs=True):
        if full_house:
            print("Testing if cards are full house")
        else:
            print("Testing if cards are same of a kind")
        same_of_kinds = {}
        # Full housea varten

        # HUOM Palauttaa tyhjän listan, jos etsitään full housea ja löydetään kolmoset, muttei paria
        # tai parin muttei kolmosia eli ei löytänyt full housea..
        full_house_cards = []
        two_pairs_list = []

        for card in cards_list:
            # Muuttaa kortin välille 0-12 riippumatta maasta
            card_number = self.biggest_card([card])
            if card_number not in same_of_kinds:
                same_of_kinds[card_number] = [card]
            else:
                same_of_kinds[card_number].append(card)

        # Järjestetään samanarvoiset pisimmästä listasta lyhyimpään
        longest_to_shortest = list(same_of_kinds.values())
        longest_to_shortest.sort(key=lambda x: len(x), reverse=True)

        for same_value_cards in longest_to_shortest:

            # Neloset
            if len(same_value_cards) >= 4:
                print("Found four of a kind")

                whats_left = [x for x in cards_list if x not in same_value_cards]

                same_value_cards = self.biggest_of_whats_left(whats_left, same_value_cards, 1)

                return same_value_cards, 7

            # Kolmoset
            if len(same_value_cards) == 3:
                print("Found three of a kind")
                # Jos halutaan tarkistaa, löytyykö vielä kolmosten lisäksi kaksi samaa
                if full_house:
                    for i in same_value_cards:
                        full_house_cards.append(i)
                    continue

                # Muuten palautetaan kolmoset ja sen lisäksi 2 muuta isointa korttia
                whats_left = [x for x in cards_list if x not in same_value_cards]
                print("Jäljellä 7 kortista, jotka ei kuulu kolmosiin", whats_left)

                same_value_cards = self.biggest_of_whats_left(whats_left, same_value_cards, 2)

                return same_value_cards, 3

            # Pari
            if len(same_value_cards) == 2:
                # Jos haluttiin löytää full house
                if full_house:
                    for i in same_value_cards:
                        full_house_cards.append(i)

                # Jos haluttiin löytää kaksi paria tai pari
                elif two_pairs:
                    for i in same_value_cards:
                        two_pairs_list.append(i)
                    continue

                # Jos ei haluttu löytää kahta paria
                elif not two_pairs:
                    print("Found pair")
                    # Muuten palautetaan pari ja sen lisäksi 3 muuta isointa korttia
                    whats_left = [x for x in cards_list if x not in same_value_cards]

                    same_value_cards = self.biggest_of_whats_left(whats_left, same_value_cards, 3)

                    return same_value_cards, 1

        # Jos etsittiin full housea
        if len(full_house_cards) == 5:
            print("Found full house")
            return full_house_cards, 6

        # Jos haluttiin löytää kaksi paria
        if two_pairs:
            if len(two_pairs_list) > 2:
                print("Found two pairs")

                # Tilanne, jossa löydetään 3 paria, etsitään 2 suurinta niistä
                if len(two_pairs_list) == 6:

                    card_values_and_cardnumbers = {}
                    for card in two_pairs_list:
                        card_value = self.biggest_card([card])
                        if card_value in card_values_and_cardnumbers:
                            card_values_and_cardnumbers[card_value].append(card)
                        else:
                            card_values_and_cardnumbers[card_value] = [card]

                    card_values_and_cardnumbers = dict(sorted(card_values_and_cardnumbers.items()))
                    card_numbers = list(card_values_and_cardnumbers.values())
                    two_pairs_list = card_numbers[0] + card_numbers[1]

                # Etsitään isoin kortti seitsemästä kortista
                # Luodaan lista, jossa ei ole kahta paria sisältäviä kortteja
                whats_left = [x for x in cards_list if x not in two_pairs_list]

                print("Jäljellä 7 kortista, jotka eivät kuulu kahden parin joukkoon", whats_left)
                two_pairs_list = self.biggest_of_whats_left(whats_left, two_pairs_list, 1)
                return two_pairs_list, 2

        # Palautetaan pari ja kolme suurinta korttia
        if len(two_pairs_list) != 0:
            print("Found pair")
            # Muuten palautetaan pari ja sen lisäksi 3 muuta isointa korttia
            whats_left = [x for x in cards_list if x not in two_pairs_list]

            print("Jäljellä 7 kortista, jotka eivät kuulu parin joukkoon", whats_left)
            two_pairs_list = self.biggest_of_whats_left(whats_left, two_pairs_list, 3)

            return two_pairs_list, 1

        # Ei löytynyt samoja kortteja
        if full_house:
            print("Didn't find full house")
        else:
            print("No same of a kind")
        return [], 0

    def biggest_of_whats_left(self, whats_left, list_to_add, number_of_cards):
        # Dict, jossa key = kortin arvo 0-13 ja value=kortin numero
        card_values_and_cardnumbers = {}
        for card in whats_left:
            card_value = self.biggest_card([card])
            card_values_and_cardnumbers[card_value] = card
        print("Korttien arvot ja numerot", card_values_and_cardnumbers)

        # Järjestetään dict korttien arvojen perusteella, pienempi=suurempi (0= Äsää 1=Kurko, ..)
        sorted_card_values_and_cardnumbers = dict(sorted(card_values_and_cardnumbers.items()))
        print("Korttien arvot ja numerot, järjestettynä", sorted_card_values_and_cardnumbers)

        # lista korteista
        card_numbers = list(sorted_card_values_and_cardnumbers.values())
        print("Lista korteista, jotka ovat arvojärjestyksessä nyt", card_numbers)

        # Uudelleen organisoidaan lista kahdeksi listaksi, jossa ensimmäisenä on samat kortit esim.
        # pari ja toisena isoimmat kortit
        lista = [[]]
        lista[0] = list_to_add.copy()
        lista1 = card_numbers[0:number_of_cards]
        lista.append(lista1)
        print("Lista, jossa on nyt halutut samat kortit ja seuraavaksi suurimmat kortit", lista)
        return lista


def main():
    player_objects = []
    for i in range(6):
        player_objects.append(Testi())

    cards = Cards()

    two_pair1, hand1 = cards.same_of_a_kind([2, 15, 7, 46, 43])
    two_pair2, hand2 = cards.same_of_a_kind([43, 41, 15, 7, 46, 29])
    two_pair3, hand3 = cards.same_of_a_kind([10, 36, 7, 46, 3, 16])

    player_objects[0].best_hand[hand1] = two_pair1
    player_objects[1].best_hand[hand2] = two_pair2
    player_objects[2].best_hand[hand3] = two_pair3

    # Dicti, jossa key on pelaajan käden arvo ja value on pelaaja objecti, että tiedetään kuka voitt
    player_hands_values = {}

    # Käydään läpi pelaajien käsien arvot ja pelaaja objectit ja lisätään ne dictiin
    for player in player_objects:
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
    # Ensimmäisen pelaajan käden arvo = "aikaisempi käsi" = ensimmäinen voittava käsi(Katso for loop
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
                player_biggest_card = cards.biggest_card(list_of_winning_cards[i])

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
            if winning_hand_value in [8, 7, 6, 4, 3, 2, 1]:
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
                        first_pair_value = cards.biggest_card(first_pair)
                        second_pair_value = cards.biggest_card(second_pair)
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
                        kicker_cards[player] = list_of_winning_cards[i][0]
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
            list_of_players = list(main_cards.keys())

            # Hain ja värin tapauksessa kaikki kortit ovat kikkereitä
            if winning_hand_value not in [5, 0]:

                # Neloset, kolmoset ja pari riittää yksi kerta
                if winning_hand_value in [7, 3, 1]:
                    loops = 1
                # Täyskäsi ja kaksi paria kaksi kierrosta
                else:
                    loops = 2

                for i in range(loops):
                    highest_card = 50

                    print("Players left", list_of_players)
                    for player in list_of_players:
                        current_card = cards.biggest_card(main_cards[player][i])

                        if current_card < highest_card:
                            highest_card = current_card
                            print("New highest card", highest_card)
                            winner_player = player

                        elif current_card == highest_card:
                            if player in list_of_players_in_tie:
                                continue
                            else:
                                if len(list_of_players_in_tie) == 0:
                                    list_of_players_in_tie = [player]
                                    # Lisätään viimeksi voitolla ollut tasapelien joukkoon.
                                    list_of_players_in_tie.append(winner_player)
                                    print("Uusi tasapeli main korteissa", list_of_players_in_tie)

                                else:
                                    list_of_players_in_tie.append(player)
                                    print("Tasapeli main korteissa", list_of_players_in_tie)

                    # Tapauksessa, että mennään toinen kierros
                    if winning_hand_value in [6, 2]:
                        # Jos kaikki vielä pelissa mukana ekan kierroksen jälkeen
                        if len(list_of_players_in_tie) == len(list_of_players) and i != 1:
                            list_of_players_in_tie.clear()
                        else:
                            # Jos pelaaja ei ole ekan kierroksen jälkeen enää mukana poistetaan se listasta, niin sitä
                            # ei vahingossa lisätä enää seuraavalle kierrokselle
                            for playeeer in main_cards:
                                if playeeer not in list_of_players_in_tie:
                                    try:
                                        list_of_players.remove(playeeer)
                                    # Jos pelaajaa ei ole kierroksen jälkeen enää listassa, on se jo poistettu
                                    except ValueError:
                                        continue

                    if winner_player not in list_of_players_in_tie and winner_player in list_of_players:
                        print("Found winner", winner_player)
                        return winner_player, False

            # Jos pääkorttien jälkeen on vielä tasapeli, ruvetaan käymään läpi kikkereitä
            if len(list_of_players_in_tie) > 1:

                # Täyskäden tapauksessa kaikki ovat main kortteja
                if winning_hand_value != 6:
                    # Tyhjennetään, jos main korteista vielä jotain jäljellä tasurissa
                    list_of_players = list_of_players_in_tie.copy()

                    for i in range(len(kicker_cards[winning_players[0]])):
                        print("Kikker korttien listan pituus", len(kicker_cards[winning_players[0]]))
                        highest_card = 50

                        # TODO  sama kuin main korteissa, lista jota käydään läpi ja poistetaan sitä mukaan kun
                        # TODO  pelaajia tippuu
                        for player in list_of_players:

                            current_card = cards.biggest_card([kicker_cards[player][i]])

                            if current_card < highest_card:
                                highest_card = current_card
                                print("Uusi korkein kortti, kikkereiden joukosta", highest_card)
                                winner_player = player

                            elif current_card == highest_card:
                                if len(list_of_players_in_tie) == 0:
                                    list_of_players_in_tie = [player]
                                else:
                                    list_of_players_in_tie.append(player)
                                print("Uusi tasapeli kikkereiden joukossa", list_of_players_in_tie)

                        # Tarkastellaan, ketkä on mukana vielä ekan kierroksen jälkeen tarkastelussa ja päivitetään
                        # ketkä kaikki käydään läpi seuraavalla iteroinnilla
                        if len(list_of_players_in_tie) == len(list_of_players) and i != len(kicker_cards[winning_players[0]]):
                            list_of_players_in_tie.clear()
                        else:
                            current_players = list_of_players.copy()
                            for player in current_players:
                                if player not in list_of_players_in_tie:
                                    try:
                                        list_of_players_in_tie.remove(player)
                                    except ValueError:
                                        continue

                        # Kierroksen jälkeen katsotaan onko voittajaa
                        if winner_player not in list_of_players_in_tie and winner_player in list_of_players:
                            print("Found winner", winner_player)
                            return winner_player, False

            if len(list_of_players_in_tie) > 1:
                print("Tasapeli", list_of_players_in_tie)
                return list_of_players_in_tie, True

            print("Voittaja", winner_player)
            return winner_player, False

    print("Winnning hands", winning_hands)
    print("Winning players cards", list_of_winning_cards)


main()
