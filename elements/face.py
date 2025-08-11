import customtkinter as ctk
from utils import MAIN_FONT, COLORS
from utils import bind_all_children

class Face(ctk.CTkFrame):

    def __init__(self, parent, controller, values, index=None):

        super().__init__(parent)
        self.controller = controller # None if owned
        self.origin = self.price = values
        self.index = index
        
        self.grid_propagate(False)
        self.configure(height=90, width=90, border_width=5, border_color='white', fg_color='silver')
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure(0, weight=1)
        
        price_frame = ctk.CTkFrame(self, fg_color='transparent')
        price_frame.grid(column=0, row=1, pady=5)
        
        # adding price labels
        k = 0
        for index, n in enumerate(values) :
            if n != 0 :
                ctk.CTkLabel(price_frame, text=n, font=(MAIN_FONT, 18), text_color=COLORS[index][1], fg_color=COLORS[index][0], corner_radius=5).pack(side='left', padx=2)
                k += 1
        
        ctk.CTkLabel(self, text='3', font=(MAIN_FONT, 22), text_color='black').grid(column=0, row=0, columnspan=k, pady=3)
        
        # making only the faces on the board clickable
        if controller is not None:
            bind_all_children(self, '<Button-1>', self.face_click)
        

    def face_click(self, event):

        # ensuring rule : player can claim 1 face card per round at most
        if self.controller.player.can_claim_face:
            # returning if the player doesn't have enough cards to claim the face
            for i in range(5):
                if self.origin[i] > len(self.controller.player.cards[i]):
                    return
            
            face = Face(self.controller.deck.cards_frame, None, self.origin)
            face.grid(column=0, row=0, sticky='n', pady=10+50*len(self.controller.player.faces))
            self.controller.player.add_face(face)
            self.controller.table_memory[-1].remove(self.origin)
            self.controller.deck.load_cards(self.controller.player)
            self.controller.board.faces_frame.rowconfigure(self.index, weight=0)
            self.destroy()
            
            self.controller.player.can_claim_face = False
            self.controller.master.score.configure(text=f'score : {self.controller.player.score}')