import customtkinter as ctk
from views  import Home, Deck, Board
from utils  import import_cards
from utils  import MAIN_FONT, INIT_THEME, COLOR_THEME
from utils  import Mode
from random import choice

ctk.set_appearance_mode(INIT_THEME)
ctk.set_default_color_theme(COLOR_THEME)

class SplendorApp(ctk.CTk):
    
    def __init__(self):

        super().__init__()
        self.geometry('1800x1000')
        self.title('Splendor')
        
        self.columnconfigure(0, weight=3, uniform='a')
        self.columnconfigure(1, weight=10, uniform='a')
        self.columnconfigure(2, weight=2, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=5, uniform='a')
        self.rowconfigure(2, weight=1, uniform='a')
        
        self.header = ctk.CTkLabel(self, text='', font=(MAIN_FONT, 42))
        self.header.grid(column=0, row=0, columnspan=3)
        self.score = ctk.CTkLabel(self, text='', font=(MAIN_FONT, 42))
        self.score.grid(column=0, row=0)
        
        self.theme = ctk.StringVar()
        self.theme_toggle = ctk.CTkSwitch(self, text=INIT_THEME, font=(MAIN_FONT, 22), variable=self.theme, command=self.update_theme, onvalue='light', offvalue='dark')
        self.theme_toggle.grid(column=2, row=0, sticky='e', padx=40)
        
        self.home = Home(self)
        self.home.grid(column=0, row=1, columnspan=3, ipady=50)
        
        self.protocol('WM_DELETE_WINDOW', self.safe_exit)
        self.mainloop()
    

    def game_begin(self):

        self.attributes('-fullscreen', True)
        self.rowconfigure(2, weight=4, uniform='a')
        self.round_over = ctk.BooleanVar()
        win = False
        
        self.table_memory = [[], [], [], []]
        self.coins = [2, 2, 2, 2, 2, 5]
        self.cards = import_cards()
        self.faces = [
            [0, 0, 4, 4, 0],
            [4, 0, 4, 0, 0],
            [3, 0, 3, 3, 0],
            [0, 0, 3, 3, 3],
            [0, 0, 0, 4, 4],
            [0, 3, 0, 3, 3],
            [0, 4, 0, 0, 4],
            [3, 3, 3, 0, 0],
            [4, 4, 0, 0, 0],
            [3, 3, 0, 0, 3]
        ]
        
        if len(self.players) == 4:
            for i in range(5):
                self.coins[i] = 7
        
        else:
            for i in range(5):
                self.coins[i] += len(self.players)
        
        for r in range(3):
            for x in range(4):
                c = choice(self.cards[r])
                self.table_memory[r].append(c)
                self.cards[r].pop(self.cards[r].index(c))
        
        for i in range(1+len(self.players)):
            f = choice(self.faces)
            self.table_memory[-1].append(f)
            self.faces.pop(self.faces.index(f))
        
        self.deck = Deck(self)
        self.deck.grid(column=0, row=2, columnspan=3, sticky='news', pady=20, padx=40)
        self.board = Board(self, self.deck)
        self.board.grid(column=0, row=1, columnspan=3, sticky='news', padx=40)
        
        while not win:            
            for player in self.players:
                self.deck.player = self.board.player = player
                player.can_claim_face = True
                
                self.deck.load_cards()
                self.deck.load_coins()
                
                self.mode = Mode.IDLE
                self.board.set_mode(Mode.IDLE)
                
                self.round_over.set(value=False)
                self.wait_variable(self.round_over)
                
                if player.score >= 15 :
                    win = True
        
        self.game_end()
    

    def game_end(self):

        self.board.destroy()
        self.deck.destroy()
        self.score.destroy()
        
        winners = [self.players[0]]
        for player in self.players[1:]:
            if player.score > winners[0].score:
                winners = [player]
            elif player.score == winners[0].score:
                if player.cards_bought() < winners[0].cards_bought():
                    winners = [player]
                elif player.cards_bought() == winners[0].cards_bought():
                    winners.append(player)
        
        if len(winners) == 1:
            self.header.configure(text='The winner is :')
        
        else:
            self.header.configure(text='The winners are :')
        
        self.rowconfigure(2, weight=4, uniform='a')
        self.middle_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.middle_frame.grid(row=1, column=1)
        
        for winner in winners:
            ctk.CTkLabel(self.middle_frame, text=winner.name, font=(MAIN_FONT, 38)).pack(anchor='center', pady=40)
    

    def update_theme(self):

        ctk.set_appearance_mode(self.theme.get())
        self.theme_toggle.configure(text=self.theme.get())
    

    def safe_exit(self):

        try:
            self.round_over.set(value=True)
        except Exception:
            pass

        self.destroy()


if __name__ == '__main__':
    SplendorApp()