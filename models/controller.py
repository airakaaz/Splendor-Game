import customtkinter as ctk
from utils    import Mode, MAIN_FONT, FACES
from utils    import clear_children, import_cards
from elements import Card, Coin
from random   import choice

class Controller():

    def __init__(self, master, board, deck):
        
        # initiating object constants
        self.master   = master
        self.board    = board
        self.deck     = deck

        # initiating object variables
        self.player   = None
        self.mode     = None
        self.wishlist = None

        # creating the aciton frame and its components
        self.action_frame = self.board.action_frame

        self.action_title = ctk.CTkLabel(self.action_frame, text='', font=(MAIN_FONT, 32))
        self.action_title.grid(column=0, row=0)

        self.middle_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.middle_frame.grid(column=0, row=1, sticky='ew', padx=10, pady=10)
        self.bottom_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.bottom_frame.grid(column=0, row=2, sticky='s', padx=10, pady=10)
        
        self.button_1 = ctk.CTkButton(self.bottom_frame, text='', font=(MAIN_FONT, 22))
        self.button_2 = ctk.CTkButton(self.bottom_frame, text='', font=(MAIN_FONT, 22))
        
        # initiating table coins
        self.coins = [2, 2, 2, 2, 2, 5]
        if len(self.master.players) == 4:
            for i in range(5): self.coins[i] = 7
        else:
            for i in range(5): self.coins[i] += len(self.master.players)
        
        # initiating table memory (stores only origins not values)
        self.table_memory = [[], [], [], []]
        self.cards = import_cards()
        self.faces = FACES

        for r in range(3):
            for x in range(4):
                c = choice(self.cards[r])
                self.table_memory[r].append(c)
                self.cards[r].remove(c)
        
        for i in range(1+len(self.master.players)):
            f = choice(self.faces)
            self.table_memory[-1].append(f)
            self.faces.remove(f)


    def set_mode(self, mode):

        # setting action frame for non IDLE modes
        def checkout_mode(title):

            self.action_title.configure(text=title)
            
            self.button_1.configure(text='cancel', command=self.wishlist_cancel)
            self.button_1.grid(column=0, row=0, padx=10, sticky='s')

            self.button_2.configure(text='confirm', state='enabled', command=self.wishlist_confirm)
            self.button_2.grid(column=1, row=0, padx=10, sticky='s')

            if self.mode == Mode.RESERVE_CARD:
                Coin(self.middle_frame, self, 5, in_action=True).pack(pady=30)
                self.button_2.configure(state='disabled')
        
        # clearing the aciton frame
        clear_children(self.middle_frame, destr=True)
        clear_children(self.bottom_frame)
        
        self.mode = mode

        match mode:
            case Mode.IDLE:
                self.action_title.configure(text='')
                self.master.header.configure(text=f'{self.player.name}\'s turn')
                self.master.score.configure(text=f'score : {self.player.score}')
                self.board.update_coins()
                
                self.button_1.configure(text='skip turn', command=self.end_of_turn)
                self.button_1.grid(column=0, row=0, padx=10, sticky='s')
                # # feature to be implemented (maybe)
                # try : self.master.after(2000, lambda: self.skip_btn.configure(state='enabled'))
                # except Exception : pass
                
            case Mode.GET_COINS:
                checkout_mode('get tokens ?')
                self.wishlist = []
            
            case Mode.GET_CARD:
                checkout_mode('buy card ?')
                self.wishlist = None
            
            case Mode.RESERVE_CARD:
                checkout_mode('reserve card ?')
                self.wishlist = None
            

    def wishlist_add(self, item):

        # if the desired item is a coin the wishlist is an array where the coins' colors are stored 
        # if the desired item is a card the wishlist is a Card object
        
        match self.mode:
            case Mode.GET_COINS:

                # adding coins to the wishlist after approval
                def approve(coin):
                    self.wishlist.append(Coin(self.middle_frame, self, coin.color, in_action=True))
                    self.wishlist[-1].pack(pady=10)
                    self.coins[coin.color] -= 1
                    self.board.update_coins()
                
                # ensuring rule : player can't have more than 10 coins
                if len(self.wishlist) + sum(self.player.coins) >= 10 : return
                
                # ensuring rule : player can only take 2 coins of the same color per round
                full = False
                if len(self.wishlist) == 2 :
                    full = (self.wishlist[0].color == self.wishlist[1].color)
                
                if len(self.wishlist) < 3 and not full:
                    if self.coins[item.color] > 0 :
                        # ensuring rule : player can only take 2 coins of the same color if there are 4 of them available
                        if item.color not in [coin.color for coin in self.wishlist]:
                            approve(item)
                        elif len(self.wishlist) == 1 :
                            if self.coins[item.color] > 2 :
                                approve(item)
            
            case Mode.GET_CARD | Mode.RESERVE_CARD:
                # saving the selected card as picked and creating a copy of it as wishlist for display
                self.picked = item
                self.wishlist = Card(self.middle_frame, self, item.origin)
                self.picked.grid_remove()
                self.wishlist.pack()

                # showing coins to be deduced from the player's balance
                if self.mode == Mode.GET_CARD:
                    for i in range(6):
                        if self.price[i] != 0 :
                            self.deck.coin_labels[1][i].configure(text=f'-{self.price[i]}')
    

    def wishlist_remove(self, coin): # coins only

        self.coins[coin.color] += 1
        self.board.update_coins()
        
        self.wishlist.remove(coin)
        coin.destroy()
        
        # auto-cancel when the wishlist is emptied
        if self.wishlist == []:
            self.set_mode(Mode.IDLE)


    def wishlist_cancel(self, force=False):

        match self.mode:
            case Mode.GET_COINS:
                # creating a buffer because lists are mutable
                wishlist_buffer = self.wishlist[:]
                for item in wishlist_buffer:
                    self.wishlist_remove(item)
            
            case Mode.GET_CARD:
                # replacing the card if it was taken from the table
                if not self.wishlist.reserved:
                    self.board.add_card(self.picked)
                # refreshing the deck to put the viewed card back where it was
                else:
                    self.deck.load_cards()
                
                # clearing the price tags
                self.deck.load_coins(self.player)
                self.wishlist = None
            
            case Mode.RESERVE_CARD:
                if self.wishlist is not None :
                    self.board.add_card(self.picked)
                    self.wishlist.destroy()
                    self.wishlist = None
                    # canceling completely when the gold coin is pressed
                    if force:
                        self.coins[-1] += 1
                    # staying in the RESERVE_CARD mode after cancelling selection
                    else:
                        self.button_2.configure(state='disabled')
                        return
                
                else:
                    self.coins[-1] += 1

        self.set_mode(Mode.IDLE)
        

    def wishlist_confirm(self):

        def replace_card(card):

            if not card.reserved :
                x = card.x
                rank = card.rank
                c = choice(self.cards[rank])

                self.cards[rank].remove(c)
                self.board.add_card(c, x, rank)
                self.table_memory[rank][x-2] = self.board.table_cards[rank][x-2].origin
                self.board.packs[rank].count_update()
            
            else:
                self.player.reserved.remove(card)
        
        match self.mode:
            case Mode.GET_COINS:
                for item in self.wishlist:
                    self.player.coins[item.color] += 1
            
            case Mode.GET_CARD:
                # creating card and adding it to the player's owned cards
                card = Card(self.deck.cards_frame, self, self.wishlist.origin, owned=True)
                card.grid(column=card.color+1, row=0, sticky='n', pady=10+50*len(self.player.cards[card.color]))
                self.player.add_card(card)

                # trying to replace the picked card
                try:
                    replace_card(self.picked)
                # leaving empty spot when no card left in pack
                except Exception: # exception raised when no card left in pack
                    self.table_memory[self.picked.rank][self.picked.x-2] = None
                
                # deducing card price from the player and adding it to the board
                for i in range(6):
                    self.coins[i] += self.price[i]
                    self.player.coins[i] -= self.price[i]
            
            case Mode.RESERVE_CARD:
                # creating card and adding it to the player's reserved cards + 1 gold coin
                card = Card(self.deck.reserved_frame, self, self.wishlist.origin, reserved=True)
                self.player.coins[-1] += 1
                self.player.reserved.append(card)

                replace_card(self.picked)
        
        # reseting the wishlist and picked variables after confirmation
        self.wishlist = None
        self.picked   = None
        self.set_mode(Mode.END_OF_TURN)


    def end_of_turn(self):
        self.master.round_ended.set(True)