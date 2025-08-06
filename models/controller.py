import customtkinter as ctk
from utils    import Mode, MAIN_FONT, FACES
from utils    import clear_children, import_cards
from elements import Card, Coin
from random   import choice

class Controller():

    def __init__(self, master, board, deck):
        
        self.master   = master
        self.board    = board
        self.deck     = deck

        self.player   = None
        self.mode     = None
        self.wishlist = None

        self.action_frame = self.board.action_frame

        self.header = ctk.CTkLabel(self.action_frame, text='', font=(MAIN_FONT, 32))
        self.header.grid(column=0, row=0)

        self.middle_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.middle_frame.grid(column=0, row=1, sticky='ew', padx=10, pady=10)
        self.bottom_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.bottom_frame.grid(column=0, row=2, sticky='s', padx=10, pady=10)
        
        self.button_1 = ctk.CTkButton(self.bottom_frame, text='', font=(MAIN_FONT, 22))
        self.button_2 = ctk.CTkButton(self.bottom_frame, text='', font=(MAIN_FONT, 22))
        
        # initiating coins
        self.coins = [2, 2, 2, 2, 2, 5]
        if len(self.master.players) == 4:
            for i in range(5): self.coins[i] = 7
        else:
            for i in range(5): self.coins[i] += len(self.master.players)
        
        # initiating table memory
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

        def buy_mode(title):

            self.header.configure(text=title)
            
            self.button_1.configure(text='cancel', command=self.wishlist_cancel)
            self.button_1.grid(column=0, row=0, padx=10, sticky='s')

            self.button_2.configure(text='confirm', command=self.wishlist_confirm)
            self.button_2.grid(column=1, row=0, padx=10, sticky='s')
        
        clear_children(self.middle_frame, destr=True)
        clear_children(self.bottom_frame)
        
        self.mode = mode

        match mode:
            case Mode.IDLE:
                self.header.configure(text='')
                self.master.header.configure(text=f'{self.player.name}\'s turn')
                self.master.score.configure(text=f'score : {self.player.score}')
                self.board.update_coins()
                
                self.button_1.configure(text='skip turn', command=self.end_of_turn)
                self.button_1.grid(column=0, row=0, padx=10, sticky='s')
                # try : self.master.after(2000, lambda: self.skip_btn.configure(state='enabled'))
                # except Exception : pass
                
            case Mode.GET_COINS:
                buy_mode('get tokens ?')
                
                self.wishlist = []
            
            case Mode.GET_CARD:
                buy_mode('buy card ?')

                self.wishlist = None
            
            case Mode.RESERVE_CARD:
                buy_mode('reserve card ?')
                
                self.board.update_coins()
                Coin(self.middle_frame, self, 5, in_action=True).pack(pady=30)
                self.button_2.configure(state='disabled')
                self.wishlist = None
                
            case Mode.END_OF_TURN:
                self.master.score.configure(text=f'score : {self.player.score}')
                self.header.configure(text='turn ended')
                
                self.button_1.configure(text='next', command=self.end_of_turn)
                self.button_1.grid(column=0, row=0, padx=10, sticky='s')
                
                self.board.update_coins()
                self.deck.load_coins(self.player)
                self.deck.load_cards(self.player)
            

    def wishlist_add(self, item):

        match self.mode:
            case Mode.GET_COINS:

                def approve(coin):
                    self.wishlist.append(Coin(self.middle_frame, self, coin.color, in_action=True))
                    self.wishlist[-1].pack(pady=10)
                    self.coins[coin.color] -= 1
                    self.board.update_coins()
                
                if len(self.wishlist) + sum(self.player.coins) >= 10 : return
                
                full = False
                
                if len(self.wishlist) == 2 :
                    full = (self.wishlist[0].color == self.wishlist[1].color)
                
                if len(self.wishlist) < 3 and not full:
                    if self.coins[item.color] > 0 :
                        if item.color not in [coin.color for coin in self.wishlist]:
                            approve(item)
                        elif len(self.wishlist) == 1 :
                            if self.coins[item.color] > 2 :
                                approve(item)
            
            case Mode.GET_CARD | Mode.RESERVE_CARD:
                self.picked = item
                self.wishlist = Card(self.middle_frame, self, item.origin)
                self.picked.grid_remove()
                self.wishlist.pack()
                self.button_2.configure(state='enabled')

                #show coins to be deduced from the player's balance
                if self.mode == Mode.GET_CARD:
                    for i in range(6):
                        if self.price[i] != 0 :
                            self.deck.coin_labels[1].configure(text=f'-{self.price[i]}')
    

    def wishlist_remove(self, coin):

        self.coins[coin.color] += 1
        self.board.update_coins()
        
        self.wishlist.remove(coin)
        coin.destroy()
        
        if self.wishlist == []:
            self.set_mode(Mode.IDLE)


    def wishlist_cancel(self, force=False):

        match self.mode:
            case Mode.GET_COINS:
                wishlist_buffer = self.wishlist[:]
                for item in wishlist_buffer:
                    self.wishlist_remove(item)
            
            case Mode.GET_CARD:
                if not self.wishlist.reserved:
                    self.board.add_card(self.picked)
                else:
                    self.deck.load_cards()
                
                self.deck.load_coins(self.player)
                self.wishlist = None
            
            case Mode.RESERVE_CARD:
                if self.wishlist != None :
                    self.board.add_card(self.picked)
                    self.wishlist.destroy()
                    self.wishlist = None
                    if force:
                        self.coins[-1] += 1
                    else:
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
                card = Card(self.deck.cards_frame, self, self.wishlist.origin, owned=True)
                card.grid(column=card.color+1, row=0, sticky='n', pady=10+50*len(self.player.cards[card.color]))
                self.player.add_card(card)
                try:
                    replace_card(self.picked)
                except Exception:
                    self.table_memory[self.picked.rank][self.picked.x-2] = None
                
                for i in range(6):
                    self.coins[i] += self.price[i]
                    self.player.coins[i] -= self.price[i]
            
            case Mode.RESERVE_CARD:
                card = Card(self.deck.reserved_frame, self, self.wishlist.origin, reserved=True)
                self.player.coins[-1] += 1
                self.player.reserved.append(card)
                replace_card(self.picked)
                
        self.wishlist = None
        self.picked   = None
        self.set_mode(Mode.END_OF_TURN)


    def end_of_turn(self):
        self.master.round_ended.set(True)