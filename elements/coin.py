import customtkinter as ctk
from utils import COIN_DIAMETER, COLORS, Mode

class Coin(ctk.CTkFrame):

    def __init__(self, parent, controller, color, in_action=False):

        super().__init__(parent)
        self.controller = controller

        self.color = color
        self.in_action = in_action

        self.configure(fg_color=COLORS[color][0], width=COIN_DIAMETER, height=COIN_DIAMETER, corner_radius=100)

        # make all coins clickable except those in the deck (they don't have a controller)
        if controller is not None : self.bind('<Button-1>', self.coin_click)


    def coin_click(self, event):

        if not self.in_action: # coin in the board
            if sum(self.controller.player.coins) < 10: # ensuring rule : player can't have more than 10 coins
                if self.color < 5 and self.controller.coins[self.color] > 0 : # the coin isn't gold and is available
                    if self.controller.mode == Mode.IDLE :
                        self.controller.set_mode(Mode.GET_COINS)
                    if self.controller.mode == Mode.GET_COINS:
                        self.controller.wishlist_add(self)
                
                # the coin is gold and available + the player has less than 3 reserved cards
                elif self.color == 5 and self.controller.coins[self.color] > 0 and len(self.controller.player.reserved) < 3 :
                    if self.controller.mode == Mode.IDLE :
                        self.controller.coins[-1] -= 1
                        self.controller.board.update_coins()
                        self.controller.set_mode(Mode.RESERVE_CARD)
        
        else: # coin in the action frame
            if self.color != 5:
                self.controller.wishlist_remove(self)
            else:
                self.controller.wishlist_cancel(force=True)