import os.path

def import_cards():
    
    file_path = f'{os.path.dirname(os.path.dirname(__file__))}/assets/splendor_cards.csv'

    try:
        cards = [[],[],[]]
        with open(file_path) as f:
            for i, card in enumerate(f):
                if i > 0:
                    values = [int(x) for x in card.split(',')]
                    cards[values[0]].append(values)
        return cards
    except Exception as e:
        print(f'failed to import cards, error :{e}')
        exit()

def clear_children(parent, destr=False):
    
    for child in parent.winfo_children():
        if destr:
            child.destroy()
        else:
            try:
                child.grid_remove()
            except Exception:
                child.pack_forget()

def bind_all_children(widget, event, function):
    widget.bind(event, function)
    for child in widget.winfo_children():
        bind_all_children(child, event, function)