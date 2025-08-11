import customtkinter as ctk
from views  import Home, Deck, Board
from utils  import MAIN_FONT, INIT_THEME, COLOR_THEME
from utils  import Mode
from models import Controller

ctk.set_appearance_mode(INIT_THEME)
ctk.set_default_color_theme(COLOR_THEME)

class SplendorApp(ctk.CTk):
    
    def __init__(self):
        
        # initiating the app
        super().__init__()
        self.geometry('1800x1000')
        self.title('Splendor')
        
        # creating the main structure of the app
        self.columnconfigure(0, weight=3, uniform='a')
        self.columnconfigure(1, weight=10, uniform='a')
        self.columnconfigure(2, weight=2, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=5, uniform='a')
        self.rowconfigure(2, weight=1, uniform='a')
        
        # creating the main top labels
        self.header = ctk.CTkLabel(self, text='', font=(MAIN_FONT, 42))
        self.header.grid(column=0, row=0, columnspan=3)

        self.score = ctk.CTkLabel(self, text='', font=(MAIN_FONT, 42))
        self.score.grid(column=0, row=0)
        
        # creating the theme toggle
        self.theme = ctk.StringVar()
        self.theme_toggle = ctk.CTkSwitch(self, text=INIT_THEME, font=(MAIN_FONT, 22), variable=self.theme, command=self.update_theme, onvalue='light', offvalue='dark')
        self.theme_toggle.grid(column=2, row=0, sticky='e', padx=40)
        
        # launching the homepage of the game
        self.home = Home(self)
        self.home.grid(column=0, row=1, columnspan=3, ipady=50)
        
        # ensuring safe exit
        self.protocol('WM_DELETE_WINDOW', self.safe_exit)
    

    def game_begin(self):

        # adjusting the window view and structure
        self.attributes('-fullscreen', True)
        self.rowconfigure(2, weight=4, uniform='a')

        # creating the flag boolean variables
        self.round_ended = ctk.BooleanVar()
        win = False
        
        # initiating the deck and board
        self.deck = Deck(self)
        self.deck.grid(column=0, row=2, columnspan=3, sticky='news', pady=20, padx=40)
        self.board = Board(self)
        self.board.grid(column=0, row=1, columnspan=3, sticky='news', padx=40)

        # initiating the game controller
        self.contoller        = Controller(self, self.board, self.deck)

        # passing the controller to the deck and board
        self.deck.controller  = self.contoller
        self.board.controller = self.contoller

        # initiating the standard elements before the game begins
        self.board.load_coins()
        self.board.load_cards()
        self.board.load_faces()
        
        # the game loop
        while not win:
            for player in self.players:
                self.contoller.player = player
                player.can_claim_face = True
                
                # loading player cards and coins
                self.deck.load_cards(player)
                self.deck.load_coins(player)
                
                # initiate the round in IDLE mode
                self.contoller.set_mode(Mode.IDLE)
                
                # setting the wait variable
                self.round_ended.set(value=False)
                self.wait_variable(self.round_ended)
                
                # verifying the win condition, the game ends after the remaining players of the cycle finish their rounds
                if player.score >= 15 : win = True
        
        # going to the end screen
        self.game_end()
    

    def game_end(self):

        # later
        self.deck.destroy()
        self.board.destroy()
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
        # updating the theme in command of the toggle
        ctk.set_appearance_mode(self.theme.get())
        self.theme_toggle.configure(text=self.theme.get())
    

    def safe_exit(self):

        # releasing the wait variable before destroying the app to avoid terminal irresponsiveness
        try:
            self.round_ended.set(value=True)
        except Exception:
            pass

        self.destroy()


# running the game when this file is executed
if __name__ == '__main__':
    SplendorApp().mainloop()