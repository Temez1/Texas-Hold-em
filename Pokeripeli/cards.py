import random


class Cardshandler:
    def __init__(self):
        self.cards = []
        self.deal_counter = 0
        self.card_on_table = []

        for i in range(52):
            self.cards.append(i)

    def draw_a_card(self):
        luku = random.choice(self.cards)
        self.cards.remove(luku)
        return luku

    def reset(self):
        # Kutsuu inittiä, eli resettaa olion
        self.__init__()

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

        # Järjestetään dict korttien arvojen mukaiseen järjestykseen (0-12)
        card_values_and_numbers = dict(sorted(card_values_and_numbers.items()))

        # Lista järjestetyistä korttien arvoista (0-13)
        list_of_card_values = list(card_values_and_numbers.keys())
        # Lista järjestetyistä korttien numeroista
        list_of_card_numbers = list(card_values_and_numbers.values())

        straight = []
        earlier_card = list_of_card_values[0] - 1

        for card in list_of_card_values:
            if (card - 1) == earlier_card:
                # Jos edellinen kortti on 2 pitää ottaa huomioon, että ässä jatkaa suoraa
                if earlier_card == 12:
                    straight.append(card_values_and_numbers[card])

                    if len(straight) == 5:
                        # Ässä on tässä tapauksessa numero 100, ettei se sekoita isointa
                        # korttia kun vertaillaan muita korttilistoja
                        lista = [100]
                        # Neljä viimeisintä korttia
                        lista.extend(list_of_card_numbers[-5:-1])
                        print("Found lower straight")
                        return lista, True

                # Jos edellinen kortti ei ollut 2 niin voidaan lisätä kortti
                else:
                    straight.append(card_values_and_numbers[card])
                    earlier_card = card
                    if len(straight) == 5:
                        print("Found straight")
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
            # Jos löydetty jo yhdet kolmoset
            if not len(full_house_cards) == 3:
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

                # Tilanne, jossa löydetään 3 paria, etsitään isoimmat kaksi
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
