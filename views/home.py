import customtkinter as ctk
from utils import MAIN_FONT
from models import Player

class Home(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)
        self.master = master
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)
        
        self.master.header.configure(text='Welcome to Splendor!')

        self.entries_frame = ctk.CTkFrame(self)
        self.entries_frame.grid(column=0, row=0, sticky='ns', ipadx=40, padx=40, pady=25)
        self.entries_frame.columnconfigure(0, weight=1)
        self.entries_frame.rowconfigure((0,1,2,3), weight=1)
        self.entries = {}
        for i in range(4):
            self.entries[i] = ctk.CTkEntry(self.entries_frame, width=360, height=40,font=(MAIN_FONT, 24), placeholder_text=f'player {i+1}')
            self.entries[i].bind('<KeyPress>', self.update_button)
            self.entries[i].grid(column=0, row=i, pady=15, padx=15)
        
        self.play_btn = ctk.CTkButton(self, font=(MAIN_FONT, 28), text='add players',state='disabled' , command=self.close_Home)
        self.play_btn.grid(column=0, row=1, ipadx=10, pady=10)
    

    def update_button(self, event):

        n=0
        for i in range(4):
            if self.entries[i].get() != '' :
                n +=1
        
        if n>1:
            if event.state == 20 and event.keycode == 36: # Ctrl + Enter
                self.close_Home()
                return
            self.play_btn.configure(text='let\'s play!', state='enabled')
        
        else:
            self.play_btn.configure(text='add players', state='disabled')
    

    def close_Home(self):

        names = []
        for entry in self.entries:
            name = self.entries[entry].get()
            if name != '':
                i = 0
                valid_name = name
                # distinguishing duplicate names
                while valid_name in names:
                    i += 1
                    valid_name = f'{name} {i}'
                names.append(valid_name)
        
        # accounting for the 1 keystroke delay when updating the button state in case of deleted name
        if len(names) < 2:
            self.play_btn.configure(text='add players', state='disabled')
            return
        
        self.master.players = [Player(name) for name in names]
        
        self.destroy()
        self.master.header.configure(text='')
        self.master.game_begin()