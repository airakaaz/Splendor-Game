import customtkinter as ctk
from utils import MAIN_FONT, COLORS
from utils import clear_children
from elements import Face, Coin

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

        self.coin_labels = [[], []]
        for i in range(6):
            k = 0 if i<3 else 3
            Coin(self.coins_frame, None, i).grid(column=1+k, row=i%3)
            self.coin_labels[0].append(ctk.CTkLabel(self.coins_frame, text='', font=(MAIN_FONT, 22), text_color=COLORS[i][0]))
            self.coin_labels[0][-1].grid(column=2+k, row=i%3)
            self.coin_labels[1].append(ctk.CTkLabel(self.coins_frame, text='', font=(MAIN_FONT, 22), text_color=COLORS[i][0]))
            self.coin_labels[1][-1].grid(column=k, row=i%3)
        

    def load_cards(self, player):

        clear_children(self.cards_frame)
        clear_children(self.reserved_frame)

        for suit in player.cards:
            for card in suit:
                card.grid()
        
        for face in player.faces:
            face.grid()
        
        for i, card in enumerate(player.reserved):
            card.grid(column=0, row=0, sticky='nw', padx=30+i*55, pady=40+i*52)


    def load_coins(self, player):

        for i in range(6):
            self.coin_labels[0][i].configure(text=player.coins[i])
            self.coin_labels[1][i].configure(text='')