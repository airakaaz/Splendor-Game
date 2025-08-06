import customtkinter as ctk
from utils import MAIN_FONT, COLORS, RANKS
from utils import Mode

class Card(ctk.CTkFrame):

    def __init__(self, parent, controller, values, x=None, owned=False, reserved=False):

        super().__init__(parent)
        self.controller = controller
        self.reserved = reserved
        self.origin = values
        self.rank = values[0]
        self.color = values[1]
        self.price = values[2:7]
        self.points = values[7]
        self.x = x
        
        self.grid_propagate(False)
        self.configure(height=160, width=128, border_width=7, border_color=COLORS[self.color][0], fg_color=RANKS[self.rank])
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=3, uniform='a')
        self.rowconfigure(0, weight=8, uniform='a')
        self.rowconfigure((1,2,3,4), weight=4, uniform='a')
        self.rowconfigure(5, weight=1, uniform='a')
        
        ctk.CTkLabel(self, text=values[7], text_color=COLORS[self.color][0], font=(MAIN_FONT, 22)).grid(column=0, row=0)
        ctk.CTkFrame(self, fg_color=COLORS[self.color][0], corner_radius=50).grid(column=1, row=0, pady=10, padx=10)
        
        k=4
        for i, p in enumerate(self.price):
            if self.price[i] > 0:
                ctk.CTkLabel(self, text=p, text_color=COLORS[i][1], font=(MAIN_FONT, 22), fg_color=COLORS[i][0], corner_radius=1000).grid(column=0, row=k, pady=3, sticky='ne')
                k -= 1
        
        if not owned:
            self.bind('<Button-1>', self.card_click)
                

    def card_click(self, event):

        def validate_card():

            price = []

            for i in range(5):
                price.append(max(self.price[i] - len(self.controller.player.cards[i]), 0))

            price.append(0)
            
            for i in range(5):
                if  price[ i] >= self.controller.player.coins[i]:
                    price[-1] += price[i] - self.controller.player.coins[i]
                    price[ i]  = self.controller.player.coins[i]

            if price[-1] > self.controller.player.coins[-1]:
                return
            
            else:
                self.controller.price = price
                self.controller.wishlist_cancel()
                self.controller.set_mode(Mode.GET_CARD)
                self.controller.wishlist_add(self)
            

        match self.controller.master.mode:
            case Mode.IDLE:
                validate_card()

            case Mode.GET_CARD:
                if self.controller.wishlist.origin == self.origin:
                    self.controller.wishlist_cancel()
                
                else:
                    validate_card()
            
            case Mode.RESERVE_CARD:
                if not self.reserved:
                    if self.controller.wishlist != None:
                        if self.controller.wishlist.origin == self.origin:
                            self.controller.wishlist_cancel()
                        
                        else:
                            self.controller.wishlist_cancel()
                            self.controller.wishlist_add(self)
                    
                    else:
                        self.controller.wishlist_add(self)