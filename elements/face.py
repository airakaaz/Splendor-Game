import customtkinter as ctk
from utils import MAIN_FONT, COLORS

class Face(ctk.CTkFrame):

    def __init__(self, parent, controller, values, i=None, owned=False):

        super().__init__(parent)
        self.controller = controller
        self.origin = self.price = values
        self.index = i
        
        self.grid_propagate(False)
        self.configure(height=90, width=90, border_width=5, border_color='white', fg_color='silver')
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure(0, weight=1)
        
        price_frame = ctk.CTkFrame(self, fg_color='transparent')
        price_frame.grid(column=0, row=1, pady=5)
        
        k = 0
        for i, n in enumerate(values) :
            if n != 0 :
                ctk.CTkLabel(price_frame, text=n, font=(MAIN_FONT, 18), text_color=COLORS[i][1], fg_color=COLORS[i][0], corner_radius=5).pack(side='left', padx=2)
                k += 1
        
        ctk.CTkLabel(self, text='3', font=(MAIN_FONT, 22), text_color='black').grid(column=0, row=0, columnspan=k, pady=3)
        
        if not owned:
            self.bind('<Button-1>', self.face_click)
        

    def face_click(self, event):

        if self.controller.player.can_claim_face:
            face = event.widget.master

            for i in range(5):
                if face.origin[i] > len(self.controller.player.cards[i]):
                    return
            
            face.pack_forget()
            self.controller.player.add_face(face.origin)
            self.controller.master.table_memory[-1].pop(face.index)
            self.controller.load_faces()
            self.controller.deck.load_cards()
            
            self.controller.player.can_claim_face = False
            self.controller.master.score.configure(text=f'score : {self.player.score}')