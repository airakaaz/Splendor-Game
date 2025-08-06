import customtkinter as ctk
from utils import MAIN_FONT, RANKS

class Pack(ctk.CTkFrame):

    def __init__(self, parent, controller, rank, rem):

        super().__init__(parent)
        self.controller = controller
        self.rank = rank
        
        self.grid_propagate(False)
        self.configure(height=160, width=128, border_width=7, border_color='white', fg_color=RANKS[self.rank])
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        ctk.CTkLabel(self, text='Splendor', text_color='white', font=(MAIN_FONT, 18)).grid(row=0, column=0, sticky='n', pady=10)
        
        dots_frame = ctk.CTkFrame(self, fg_color='transparent')
        dots_frame.grid(row=0, column=0, sticky='s', pady=12)
        for dot in range(3-rank):
            ctk.CTkFrame(dots_frame, height=15, width=15, fg_color='white', corner_radius=100).pack(side='left', padx=3)
        
        self.remaining = ctk.CTkLabel(self, text=rem, text_color='black', font=(MAIN_FONT, 42))    
        self.remaining.grid(column=0, row=0)
    

    def count_update(self):

        self.remaining.configure(text=len(self.controller.cards[self.rank]))
        if len(self.controller.cards[self.rank]) == 0 :
            self.destroy()