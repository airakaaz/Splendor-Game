import customtkinter as ctk
from utils import COIN_DIAMETER, COLORS, Mode

class Coin(ctk.CTkFrame):

    def __init__(self, parent, controller, color, active=True, in_action=False):

        super().__init__(parent)
        self.controller = controller

        self.color = color
        self.in_action = in_action

        self.configure(fg_color=COLORS[color][0], width=COIN_DIAMETER, height=COIN_DIAMETER, corner_radius=100)
        if active : self.bind('<Button-1>', self.coin_click)


    def coin_click(self, event):

        if not self.in_action:
            if sum(self.controller.player.coins) < 10:
                if self.color < 5 and self.controller.coins[self.color] > 0 :
                    if self.controller.mode == Mode.IDLE :
                        self.controller.set_mode(Mode.GET_COINS)
                    if self.controller.mode == Mode.GET_COINS:
                        self.controller.wishlist_add(self)
                        
                elif self.color == 5 and self.controller.coins[self.color] > 0 and len(self.controller.player.reserved) < 3 :
                    match self.controller.mode:
                        case Mode.IDLE :
                            self.controller.coins[-1] -= 1
                            self.controller.set_mode(Mode.RESERVE_CARD)
        
        else:
            if self.color != 5:
                self.controller.wishlist_remove(self)
            else:
                self.controller.wishlist_cancel(force=True)