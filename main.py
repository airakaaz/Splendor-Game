import customtkinter as ctk
from views  import Home, Deck, Board
from utils  import MAIN_FONT, INIT_THEME, COLOR_THEME
from utils  import Mode
from models import Controller

ctk.set_appearance_mode(INIT_THEME)
ctk.set_default_color_theme(COLOR_THEME)

class SplendorApp(ctk.CTk):
    
    def __init__(self):

        # allowing implementaton of quick debugging code that can be turned off easily ex:(if master.DEBUG : do_stuff)
        self.DEBUG = False

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
        self.controller        = Controller(self, self.board, self.deck)

        # passing the controller to the deck and board
        self.deck.controller  = self.controller
        self.board.controller = self.controller

        # initiating the standard elements before the game begins
        self.board.load_coins()
        self.board.load_cards()
        self.board.load_faces()

        if self.DEBUG:
            from elements import Card, Face
            from utils import FACES
            from random import choice
            for player in self.players:
                for _ in range(4):
                    card_origin = choice(self.controller.cards[0])
                    card = Card(self.deck.cards_frame, self.controller, card_origin, owned=True)
                    card.grid(column=card.color+1, row=0, sticky='n', pady=10+50*len(player.cards[card.color]))
                    player.add_card(card)
                
                for _ in range(2):
                    face_origin = choice(FACES)
                    face = Face(self.controller.deck.cards_frame, None, face_origin)
                    face.grid(column=0, row=0, sticky='n', pady=10+50*len(player.faces))
                    player.add_face(face)
        
        # the game loop
        while not win:
            for player in self.players:
                self.controller.player = player
                player.can_claim_face = True
                
                # loading player cards and coins
                self.deck.load_cards(player)
                self.deck.load_coins(player)
                
                # initiate the round in IDLE mode
                self.controller.set_mode(Mode.IDLE)
                
                # setting the wait variable
                self.round_ended.set(value=False)
                self.wait_variable(self.round_ended)
                
                # verifying the win condition, the game ends after the remaining players of the cycle finish their rounds
                if player.score >= 15 : win = True
        
        # going to the end screen
        self.game_end()
    

    def game_end(self):

        self.header.configure(text='GAME ENDED')
        self.controller.mode = Mode.GAME_ENDED

        # clearing the screen
        self.deck.destroy()
        self.board.action_frame.destroy()
        self.board.coins_frame.destroy()
        self.score.configure(text='')
        
        # sorting and ranking the players
        self.players.sort(key=lambda player : player.cards_bought())
        self.players.sort(key=lambda player : player.score, reverse=True)

        rank = 1
        self.players[0].rank = rank
        for i in range(1, len(self.players)):
            same_score = self.players[i].score == self.players[i-1].score
            same_cards_bought = self.players[i].cards_bought() == self.players[i-1].cards_bought()
            if same_score:
                if same_cards_bought:
                    pass # not incrementing rank in case of tie
            else:
                rank += 1
            self.players[i].rank = rank

        # making the layout
        ## decks viewer
        self.decks_viewer = ctk.CTkTabview(self)
        self.decks_viewer._segmented_button.configure(font=(MAIN_FONT, 22))
        self.decks_viewer.grid(column=0, row=2, columnspan=3, sticky='news', pady=20, padx=40)

        for player in self.players:

            name = f'  {player.name}  ' # quick nd dirty way to add spacing in the tabview's segmented button
            self.decks_viewer.add(name)
            self.decks_viewer.tab(name).columnconfigure(0, weight=1)
            self.decks_viewer.tab(name).rowconfigure(0, weight=1)

            deck = Deck(self.decks_viewer.tab(name))
            player.migrate_cards(deck)
            deck.load_coins(player)
            deck.load_cards(player)
            deck.grid(column=0, row=0, sticky="news")

        ## leaderboad
        leaderboard = ctk.CTkFrame(self.board)
        leaderboard.grid(column=0, row=0, sticky='news', padx=20, pady=10)

        leaderboard.columnconfigure((0,1,2), weight=1)
        leaderboard.rowconfigure(1, weight=1)

        ranks = ctk.CTkFrame(leaderboard, fg_color="transparent")
        ranks.grid(column=0, row=1, rowspan=3, sticky="ew")

        names = ctk.CTkFrame(leaderboard, fg_color="transparent")
        names.grid(column=1, row=1, rowspan=3, sticky="ew")

        scores = ctk.CTkFrame(leaderboard, fg_color="transparent")
        scores.grid(column=2, row=1, rowspan=3, sticky="ew")

        ctk.CTkLabel(leaderboard, text='rank'  , font=(MAIN_FONT, 28)).grid(column=0, row=0, padx=40, pady=(40,0))
        ctk.CTkLabel(leaderboard, text='player', font=(MAIN_FONT, 28)).grid(column=1, row=0, padx=40, pady=(40,0))
        ctk.CTkLabel(leaderboard, text='score' , font=(MAIN_FONT, 28)).grid(column=2, row=0, padx=40, pady=(40,0))
        
        for i, player in enumerate(self.players):
            ctk.CTkLabel(ranks , text=player.rank , font=(MAIN_FONT, 24)).pack(pady=20)
            ctk.CTkLabel(names , text=player.name , font=(MAIN_FONT, 24)).pack(pady=20)
            ctk.CTkLabel(scores, text=player.score, font=(MAIN_FONT, 24)).pack(pady=20)

        ## buttons
        buttons_frame = ctk.CTkFrame(self.board, fg_color='transparent')
        buttons_frame.grid(column=2, row=0, sticky='news', padx=20, pady=10)
        buttons_frame.rowconfigure((0,1,2), weight=1)
        buttons_frame.columnconfigure(0, weight=1)

        restart_button = ctk.CTkButton(buttons_frame, text='play\nagain'    , font=(MAIN_FONT, 22), command=self.game_restart)
        restart_button.grid(column=0, row=0, sticky='news', pady=20, padx=20)

        reset_button   = ctk.CTkButton(buttons_frame, text='change\nplayers', font=(MAIN_FONT, 22), command=self.game_reset)
        reset_button.grid(column=0, row=1, sticky='news', pady=20, padx=20)

        exit_button    = ctk.CTkButton(buttons_frame, text='exit\ngame'     , font=(MAIN_FONT, 22), command=self.safe_exit)
        exit_button.grid(column=0, row=2, sticky='news', pady=20, padx=20)
    

    def update_theme(self):
        # updating the theme in command of the toggle
        ctk.set_appearance_mode(self.theme.get())
        self.theme_toggle.configure(text=self.theme.get())
    

    def game_restart(self):

        for player in self.players:
            player.__init__(player.name)
        
        self.board.destroy()
        self.decks_viewer.destroy()
        self.game_begin()
    

    def game_reset(self):

        self.board.destroy()
        self.decks_viewer.destroy()
        self.rowconfigure(2, weight=1, uniform='a')

        self.home = Home(self)
        self.home.grid(column=0, row=1, columnspan=3, ipady=50)
    

    def safe_exit(self):

        # releasing the wait variable before destroying the app to avoid terminal irresponsiveness
        try:
            self.round_ended.set(value=True)
        except Exception:
            pass

        self.destroy()


# running the game when this file is executed
if __name__ == '__main__':
    game = SplendorApp()
    game.mainloop()