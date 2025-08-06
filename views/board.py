import customtkinter as ctk
from elements import Card, Face, Pack, Coin
from utils    import MAIN_FONT, COLORS
from utils    import Mode

class Board(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)
        self.controller = None
        
        self.configure(fg_color='transparent')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3, uniform='a')
        self.columnconfigure(1, weight=10, uniform='a')
        self.columnconfigure(2, weight=2, uniform='a')
        
        self.coins_frame = ctk.CTkFrame(self)
        self.coins_frame.grid(column=2, row=0, sticky='news', padx=20, pady=10)
        self.coins_frame.columnconfigure((0,1,2), weight=1, uniform='a')
        self.coins_frame.rowconfigure((0,1,2,3,4,5), weight=1, uniform='a')
        
        self.cards_frame = ctk.CTkFrame(self)
        self.cards_frame.grid(column=1, row=0, sticky='news', padx=100, pady=10)
        self.cards_frame.rowconfigure((0,1,2), weight=1, uniform='a')
        self.cards_frame.columnconfigure(0, weight=3, uniform='a')
        self.cards_frame.columnconfigure((1,2,3,4,5), weight=2, uniform='a')
        
        self.faces_frame = ctk.CTkFrame(self.cards_frame, fg_color='transparent')
        self.faces_frame.grid(column=0, row=0, rowspan=3)
        
        self.action_frame = ctk.CTkFrame(self, )
        self.action_frame.grid(column=0, row=0, sticky='news', padx=20, pady=10)
        self.action_frame.rowconfigure((0,2), weight=1, uniform='a')
        self.action_frame.rowconfigure(1, weight=5, uniform='a')
        self.action_frame.columnconfigure(0, weight=1)


    def add_card(self, c, x=None, rank=None):

        if type(c) == Card:
            c.grid(column=c.x, row=c.rank)
        else:
            card = Card(self.cards_frame, self.controller, c, x)
            card.grid(column=x, row=rank)
            self.table_cards[rank][x-2] = card


    def load_cards(self):

        self.packs = []

        for x in range(3):
            self.packs.append(Pack(self.cards_frame, self.controller, x, len(self.controller.cards[x])))
            self.packs[x].grid(column=1, row=x)
        
        self.table_cards = [[], [], []]
        for r in range(3):
            for x in range(4):
                self.table_cards[r].append(None)
                self.add_card(self.controller.table_memory[r][x], x+2, r)


    def load_faces(self):

        self.table_faces = []

        pad = 3 + 10 * (5-len(self.controller.table_memory[-1]))
        for i,face in enumerate(self.controller.table_memory[-1]):
            self.table_faces.append(Face(self.faces_frame, self.controller, face, i))
            self.table_faces[-1].pack(pady=pad)


    def load_coins(self):

        self.coins = []
        for color in range(6):
            Coin(self.coins_frame, self.controller, color).grid(column=1, row=color)
            self.coins.append(ctk.CTkLabel(self.coins_frame, text=self.controller.coins[color], font=(MAIN_FONT, 22), text_color=COLORS[color][0]))
            self.coins[-1].grid(column=2, row=color)

    def update_coins(self):

        for color in range(6):
            self.coins[color].configure(text=self.controller.coins[color])