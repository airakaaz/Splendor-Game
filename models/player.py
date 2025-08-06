class Player():

    def __init__(self, name):

        self.name = name
        self.coins = [0, 0, 0, 0, 0, 0]
        self.cards = [[], [], [], [], []]
        self.reserved = []
        self.faces = []
        self.score = 0

    
    def add_card(self, card):

        self.cards[card[1]].append(card)
        self.score += card[7]
    

    def add_face(self, face):

        self.faces.append(face)
        self.score += 3
    

    def cards_bought(self):

        return sum(len(suit) for suit in self.cards)