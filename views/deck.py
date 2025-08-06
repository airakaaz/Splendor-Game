import customtkinter as ctk
from utils import MAIN_FONT, COLORS, COIN_DIAMETER
from utils import clear_children, clear_grid
from elements import Card, Face

class Deck(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)
        self.controller = None
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3, uniform='a')
        self.columnconfigure(1, weight=10, uniform='a')
        self.columnconfigure(2, weight=3, uniform='a')
        
        self.reserved_frame = ctk.CTkFrame(self, )
        self.reserved_frame.grid(column=0, row=0, sticky='news', padx=20, pady=10)
        self.reserved_frame.rowconfigure(0, weight=0)
        self.reserved_frame.columnconfigure(0, weight=0)
        
        self.coins_frame = ctk.CTkFrame(self)
        self.coins_frame.grid(column=2, row=0, sticky='news', padx=20, pady=10)
        self.coins_frame.columnconfigure((1,4), weight=4, uniform='a')
        self.coins_frame.columnconfigure((0,2,3,5), weight=3, uniform='a')
        self.coins_frame.rowconfigure((0,1,2), weight=1, uniform='a')
        
        self.cards_frame = ctk.CTkFrame(self)
        self.cards_frame.grid(column=1, row=0, sticky='news', padx=100, pady=10)
        self.cards_frame.rowconfigure(0, weight=0, uniform='a')
        self.cards_frame.columnconfigure(0, weight=3, uniform='a')
        self.cards_frame.columnconfigure((1,2,3,4,5), weight=2, uniform='a')
        

    def load_cards(self, player):

        clear_grid(self.cards_frame)
        clear_children(self.reserved_frame)

        for suit in player.cards:
            for card in suit:
                card.grid()
        
        pad = 10
        for face in player.faces:
            Face(self.cards_frame, self.controller.board, face, owned=True).grid(column=0, row=0, sticky='n', pady=pad)
            pad += 50
        
        self.reserved = []
        for i, card in enumerate(player.reserved):
            self.reserved.append(Card(self.reserved_frame, self.controller, card, i, reserved=True))
            self.reserved[-1].grid(column=0, row=0, sticky='nw', padx=30+i*55, pady=40+i*52)


    def load_coins(self, player):

        clear_children(self.coins_frame)
        self.coins = [[], []]

        for i in range(6):
            k = 0 if i<3 else 3
            ctk.CTkFrame(self.coins_frame, fg_color=COLORS[i][0], width=COIN_DIAMETER, height=COIN_DIAMETER, corner_radius=100).grid(column=1+k, row=i%3)
            ctk.CTkLabel(self.coins_frame, text=player.coins[i], font=(MAIN_FONT, 22), text_color=COLORS[i][0]).grid(column=2+k, row=i%3)
