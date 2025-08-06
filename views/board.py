import customtkinter as ctk
from elements import Card, Face, Pack
from utils    import clear_children
from utils    import MAIN_FONT, COLORS, COIN_DIAMETER
from utils    import Mode
from random   import choice

class Board(ctk.CTkFrame):

    def __init__(self, master, deck, player=None):

        super().__init__(master)
        self.master = master
        self.deck = deck
        self.player = player
        
        self.configure(fg_color='transparent')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3, uniform='a')
        self.columnconfigure(1, weight=10, uniform='a')
        self.columnconfigure(2, weight=2, uniform='a')
        
        self.coins_frame = ctk.CTkFrame(self)
        self.coins_frame.grid(column=2, row=0, sticky='news', padx=20, pady=10)
        self.coins_frame.columnconfigure((0,1,2), weight=1, uniform='a')
        self.coins_frame.rowconfigure((0,1,2,3,4,5), weight=1, uniform='a')
        self.load_coins()
        
        self.cards_frame = ctk.CTkFrame(self)
        self.cards_frame.grid(column=1, row=0, sticky='news', padx=100, pady=10)
        self.cards_frame.rowconfigure((0,1,2), weight=1, uniform='a')
        self.cards_frame.columnconfigure(0, weight=3, uniform='a')
        self.cards_frame.columnconfigure((1,2,3,4,5), weight=2, uniform='a')
        
        self.packs = []
        for x in range(3):
            self.packs.append(Pack(self.cards_frame, self.master, x, len(self.master.cards[x])))
            self.packs[x].grid(column=1, row=x)
        
        self.table_cards = [[], [], []]
        for r in range(3):
            for x in range(4):
                self.table_cards[r].append(None)
                self.add_card(x+2, r, self.master.table_memory[r][x])
        
        self.faces_frame = ctk.CTkFrame(self.cards_frame, fg_color='transparent')
        self.faces_frame.grid(column=0, row=0, rowspan=3)
        self.load_faces()
        
        self.action_frame = ctk.CTkFrame(self, )
        self.action_frame.grid(column=0, row=0, sticky='news', padx=20, pady=10)
        self.action_frame.rowconfigure((0,2), weight=1, uniform='a')
        self.action_frame.rowconfigure(1, weight=5, uniform='a')
        self.action_frame.columnconfigure(0, weight=1)


    def add_card(self, x, rank, c):

        card = Card(self.cards_frame, self, c, x)
        card.grid(column=x, row=rank)
        self.table_cards[rank][x-2] = card
    

    def load_faces(self):

        clear_children(self.faces_frame)
        self.table_faces = []

        pad = 3 + 10 * (5-len(self.master.table_memory[-1]))
        for i,face in enumerate(self.master.table_memory[-1]):
            self.table_faces.append(Face(self.faces_frame, self, face, i))
            self.table_faces[-1].pack(pady=pad)
    

    def load_coins(self):

        clear_children(self.coins_frame)
        self.coins = []

        for i in range(6):
            self.coins.append([])
            self.coins[i].append(ctk.CTkFrame(self.coins_frame, fg_color=COLORS[i][0], width=COIN_DIAMETER, height=COIN_DIAMETER, corner_radius=100))
            self.coins[i].append(ctk.CTkLabel(self.coins_frame, text=self.master.coins[i], font=(MAIN_FONT, 22), text_color=COLORS[i][0]))
            self.coins[i][0].grid(column=1, row=i)
            self.coins[i][1].grid(column=2, row=i)
            self.coins[i][0].bind('<Button-1>', self.coin_click)
    

    def coin_click(self, event):

        for i in range(6):
            if str(self.coins[i][0]) == event.widget.winfo_parent():
                id = i
                break
        
        if sum(self.player.coins) < 10:
            if id < 5 and self.master.coins[id] > 0 :
                if self.master.mode == Mode.IDLE :
                    self.set_mode(Mode.GET_COINS)
                if self.master.mode == Mode.GET_COINS:
                    self.wishlist_add(id)
            elif id == 5 and self.master.coins[id] > 0 and len(self.player.reserved) < 3 :
                if self.master.mode == Mode.IDLE :
                    self.master.coins[-1] -= 1
                    self.set_mode(Mode.RESERVE_CARD)
    

    def set_mode(self, mode):

        def buy_mode(title):

            self.header.configure(text=title)
            
            self.middle_frame.grid(column=0, row=1, sticky='ew', padx=10, pady=10)
            self.bottom_frame.grid(column=0, row=2, sticky='s', padx=10, pady=10)
            
            self.cancel_btn = ctk.CTkButton(self.bottom_frame, text='cancel', font=(MAIN_FONT, 22), command=self.wishlist_cancel)
            self.cancel_btn.pack(side='left', padx=10, anchor='s')
            self.confirm_btn = ctk.CTkButton(self.bottom_frame, text='confirm', font=(MAIN_FONT, 22), command=self.wishlist_confirm)
            self.confirm_btn.pack(side='left', padx=10, anchor='s')
        

        clear_children(self.action_frame)
        self.header = ctk.CTkLabel(self.action_frame, text='', font=(MAIN_FONT, 32))
        self.header.grid(column=0, row=0)
        self.middle_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.bottom_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        
        self.master.mode = mode

        match mode:
            case Mode.IDLE: # idle
                self.header.configure(text='')
                self.master.header.configure(text=f'{self.player.name}\'s turn')
                self.master.score.configure(text=f'score : {self.player.score}')
                self.load_coins()
                
                self.bottom_frame.grid(column=0, row=2, sticky='s', padx=10, pady=10)
                self.skip_btn = ctk.CTkButton(self.bottom_frame, text='skip turn', state='enabled', font=(MAIN_FONT, 22), command=self.end_of_turn)
                self.skip_btn.pack(side='left', padx=10, anchor='s')
                # try : self.after(2000, lambda: self.skip_btn.configure(state='enabled'))
                # except Exception : pass
                
            case Mode.GET_COINS: # get coins
                buy_mode('get tokens ?')
                
                self.wishlist = [[], []]
            
            case Mode.GET_CARD: # get card
                buy_mode('buy card ?')
                
                self.wishlist = None
            
            case Mode.RESERVE_CARD: # reserve card
                buy_mode('reserve card ?')
                
                self.load_coins()
                ctk.CTkFrame(self.middle_frame, fg_color=COLORS[5][0], width=COIN_DIAMETER, height=COIN_DIAMETER, corner_radius=100).pack(pady=30)
                self.confirm_btn.configure(state='disabled')
                self.wishlist = None
                
            case Mode.END_OF_TURN: # end of turn
                self.master.score.configure(text=f'score : {self.player.score}')
                self.header.configure(text='turn ended')
                
                self.bottom_frame.grid(column=0, row=2, sticky='s', padx=10, pady=10)
                self.next_btn = ctk.CTkButton(self.bottom_frame, text='next', font=(MAIN_FONT, 22), command=self.end_of_turn)
                self.next_btn.pack(side='left', padx=10, anchor='s')
                
                self.load_coins()
                self.deck.load_coins()
                self.deck.load_cards()
            

    def wishlist_add(self, item):

        match self.master.mode:
            case Mode.GET_COINS:
                def approve(c):

                    self.wishlist[0].append(c)
                    self.wishlist[1].append(ctk.CTkFrame(self.middle_frame, fg_color=COLORS[c][0], width=COIN_DIAMETER, height=COIN_DIAMETER, corner_radius=100))
                    self.wishlist[1][-1].pack(pady=10)
                    self.wishlist[1][-1].bind('<Button-1>', self.wishlist_remove)

                    self.master.coins[c] -= 1
                    self.load_coins()
                
                if len(self.wishlist[0]) + sum(self.player.coins) >= 10 : return
                
                full = False
                
                if len(self.wishlist[0]) == 2 :
                    full = (self.wishlist[0][0] == self.wishlist[0][1])
                
                if len(self.wishlist[0]) < 3:
                    if self.master.coins[item] > 0 :
                        if item not in self.wishlist[0] and not full :
                            approve(item)
                        elif len(self.wishlist[0]) == 1 :
                            if self.master.coins[item] > 2 :
                                approve(item)
            
            case _:
                if item.reserved:
                    self.wishlist = self.deck.reserved[item.x]
                
                else:
                    self.wishlist = item

                self.wishlist.grid_forget()
                Card(self.middle_frame, self, item.origin).pack()
                self.confirm_btn.configure(state='enabled')

                if self.master.mode == Mode.GET_CARD:
                    for i in range(6):
                        k = 0
                        if i>2 : k=3
                        if self.price[i] != 0 :
                            ctk.CTkLabel(self.deck.coins_frame, text=f'-{self.price[i]}',text_color=COLORS[i][0], font=(MAIN_FONT, 22)).grid(column=0+k, row=i%3)
    

    def wishlist_remove(self, event=None, id=None):

        if id == None:
            for i, widget in enumerate(self.wishlist[1]):
                if str(widget) == event.widget.winfo_parent():
                    id = i
                    break
        
        self.master.coins[self.wishlist[0][id]] += 1
        self.load_coins()
        
        self.wishlist[0].pop(id)
        self.wishlist[1][id].destroy()
        self.wishlist[1].pop(id)
        
        if self.wishlist[0] == []:
            self.set_mode(Mode.IDLE)


    def wishlist_cancel(self):

        match self.master.mode:
            case Mode.GET_COINS:
                for i in range(len(self.wishlist[0])):
                    self.wishlist_remove(id=0)
            
            case Mode.GET_CARD:
                if type(self.wishlist) == Card:
                    if not self.wishlist.reserved:
                        self.add_card(self.wishlist.x, self.wishlist.rank, self.wishlist.origin)
                    
                    else:
                        self.deck.load_cards()
                
                else:
                    self.load_faces()
                
                self.deck.load_coins()
                self.wishlist = None
            
            case Mode.RESERVE_CARD:
                if self.wishlist != None :
                    self.add_card(self.wishlist.x, self.wishlist.rank, self.wishlist.origin)
                    self.set_mode(Mode.RESERVE_CARD)
                    return
                
                else:
                    self.master.coins[-1] += 1

        self.set_mode(Mode.IDLE)
        

    def wishlist_confirm(self):

        def replace_card(card):

            x, rank = card.x, card.rank

            if not card.reserved :
                c = choice(self.master.cards[rank])

                self.master.cards[rank].pop(self.master.cards[rank].index(c))
                self.add_card(x, rank, c)
                self.master.table_memory[rank][x-2] = self.table_cards[rank][x-2].origin
                self.packs[rank].count_update()
            
            else:
                self.player.reserved.pop(x)
        
        match self.master.mode:
            case Mode.GET_COINS:
                for item in self.wishlist[0]:
                    self.player.coins[item] += 1
            
            case Mode.GET_CARD:
                self.player.add_card(self.wishlist.origin)
                try:
                    replace_card(self.wishlist)
                except Exception:
                    self.master.table_memory[self.wishlist.rank][self.wishlist.x-2] = None
                    self.wishlist = None
                
                for i in range(6):
                    self.master.coins[i] += self.price[i]
                    self.player.coins[i] -= self.price[i]
            
            case Mode.RESERVE_CARD:
                self.player.coins[-1] += 1
                self.player.reserved.append(self.wishlist.origin)
                replace_card(self.wishlist)
                
        self.set_mode(Mode.END_OF_TURN)
        

    def end_of_turn(self):

        self.master.round_over.set(True)
