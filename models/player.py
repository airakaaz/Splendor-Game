from elements import Card, Face

class Player():

    def __init__(self, name):

        self.name = name
        self.coins = [0, 0, 0, 0, 0, 0]
        self.cards = [[], [], [], [], []]
        self.reserved = []
        self.faces = []
        self.score = 0

    
    def add_card(self, card):

        self.cards[card.color].append(card)
        self.score += card.points
    

    def add_face(self, face):

        self.faces.append(face)
        self.score += 3
    

    def cards_bought(self):

        return sum(len(suit) for suit in self.cards)
    
    
    def migrate_cards(self, new_deck):

        final_cards = [[], [], [], [], []]
        for suit in self.cards:
            for card in suit:
                new_card = Card(new_deck.cards_frame, None, card.origin, owned=True)
                new_card.grid(column=card.color+1, row=0, sticky='n', pady=10+50*len(final_cards[card.color]))
                final_cards[card.color].append(new_card)
        self.cards = final_cards

        final_faces = []
        for face in self.faces:
            new_face = Face(new_deck.cards_frame, None, face.origin)
            new_face.grid(column=0, row=0, sticky='n', pady=10+50*len(final_faces))
            final_faces.append(new_face)
        self.faces = final_faces

        final_reserved = []
        for card in self.reserved:
            card = Card(new_deck.reserved_frame, None, card.origin, reserved=True)
            final_reserved.append(card)
        self.reserved = final_reserved