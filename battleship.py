import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path
import os
import glob


def save_private_game_state(callsign, state, mycallsign):
    home = str(Path.home())

    if callsign == mycallsign:
        private_filepath = os.path.join(home, f"battleship-{callsign}_private.txt")
        with open(private_filepath, 'w') as file:
            for row in state:
                file.write(''.join(row) + '\n')


def save_public_game_state(callsign, state, mycallsign):
    home = str(Path.home())
    dropbox_path = os.path.join(home, 'Dropbox')

    if callsign == mycallsign:
        public_filepath = os.path.join(dropbox_path, f"battleship-{callsign}.txt")
        with open(public_filepath, 'w') as file:
            for row in state:
                file.write(''.join([cell.lower() for cell in row]) + '\n')


def save_opponent_public_state(callsign, state, mycallsign):
    home = str(Path.home())

    if callsign != mycallsign:
        opponent_filepath = os.path.join(home, f"battleship-{callsign}.txt")
        with open(opponent_filepath, 'w') as file:
            for row in state:
                file.write(''.join(row) + '\n')


def load_game_state(fname, battleship_type):
    home = str(Path.home())
    filepath = os.path.join(home, fname)

    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()

        if not lines:
            state = [['b'] * 10 for _ in range(10)]
            view_only_state = [['b'] * 10 for _ in range(10)]
        else:
            state = [list(line.strip()) for line in lines]
            if battleship_type == "private":
                view_only_state = [[char.lower() for char in row] for row in state]
            else:
                view_only_state = state
    else:
        if "_private.txt" in filepath:  # do not create a new private file for opponents
            state = [['b'] * 10 for _ in range(10)]
            view_only_state = [['b'] * 10 for _ in range(10)]
        else:
            return None, None, None

    callsign = fname.replace("battleship-", "").replace(home + "/", "").replace("_private.txt", "").replace(".txt", "")
    return state, view_only_state, callsign


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack_forget()


def reset_grid(frame, state, callsign, mycallsign, labels):
    if not messagebox.askokcancel("Confirmation", "Do you really want to reset the game?"):
        return

    for i in range(10):
        for j in range(10):
            state[i][j] = 'b'
            labels[i][j].config(text='b', bg='light blue')  # Update the grid cell's text and color

    save_private_game_state(callsign, state, mycallsign)
    save_public_game_state(callsign, state, mycallsign)


def create_gui(state, view_only_state, callsign, root, mycallsign):
    frame = tk.Frame(root)
    frame.pack(side="left", padx=5, pady=5)
    grid_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    def on_click(i, j, label, callsign, state, view_only_state):
        if state[i][j].islower():
            lower_state = state[i][j].lower()
            if lower_state == 'b':
                state[i][j] = 'm'
                label.configure(bg='white', text=' ')
            elif lower_state == 'm':
                state[i][j] = 'h'
                label.configure(bg='red', text=' ')
            elif lower_state == 'h':
                state[i][j] = 's'
                label.configure(bg='black', text=' ')
            elif lower_state == 's':
                state[i][j] = 'b'
                label.configure(bg='light blue', text=' ')
        else:
            if state[i][j] == 'B':
                state[i][j] = 'H'
                label.configure(bg='red', text='⚓')
            elif state[i][j] == 'H':
                state[i][j] = 'S'
                label.configure(bg='black', text='⚓')
            elif state[i][j] == 'S':
                state[i][j] = 'B'
                label.configure(bg='light blue', text='⚓')

        if callsign == mycallsign:
            save_private_game_state(callsign, state, mycallsign)
            save_public_game_state(callsign, state, mycallsign)
        else:
            save_opponent_public_state(callsign, state, mycallsign)

    def on_right_click(i, j, label, callsign, state, view_only_state):
        if state[i][j].islower():
            state[i][j] = state[i][j].upper()
            if state[i][j] != 'M':
                label.configure(text='⚓')
        else:
            state[i][j] = state[i][j].lower()
            label.configure(text=' ')

        if callsign == mycallsign:
            save_private_game_state(callsign, state, mycallsign)
            save_public_game_state(callsign, state, mycallsign)

    for j in range(10):
        tk.Label(frame, text=str(j + 1)).grid(row=0, column=j + 1)

    for i in range(10):
        tk.Label(frame, text=grid_labels[i]).grid(row=i + 1, column=0)

    for i in range(10):
        for j in range(10):
            color = ('light blue' if state[i][j].lower() == 'b' else
                     'white' if state[i][j].lower() == 'm' else
                     'red' if state[i][j].lower() == 'h' else 'black')
            text = '⚓' if state[i][j].isupper() else ' '
            label = tk.Label(frame, width=2, height=1, bg=color, text=text)
            label.grid(row=i + 1, column=j + 1, padx=1, pady=1)
            label.bind('<Button-1>', lambda event, i=i, j=j, label=label, callsign=callsign, state=state,
                                            view_only_state=view_only_state: on_click(i, j, label, callsign, state,
                                                                                      view_only_state))
            label.bind('<Button-3>', lambda event, i=i, j=j, label=label, callsign=callsign, state=state,
                                            view_only_state=view_only_state: on_right_click(i, j, label, callsign,
                                                                                            state, view_only_state))

    reset_button = tk.Button(frame, text=f'Reset {callsign}', command=lambda: reset_grid(frame, state, callsign, mycallsign, labels))
    reset_button.grid(row=12, column=1, columnspan=10, sticky='nsew')

    return frame

def main():
    home = str(Path.home())
    battleship_files = glob.glob(home + "/battleship-*.txt")

    root = tk.Tk()
    root.title("Battleship Game")

    USER_PRIVATE_FILE = [file for file in battleship_files if "_private.txt" in file]
    OTHER_FILES = [file for file in battleship_files if "_private.txt" not in file]
    OTHER_FILES.sort(key=lambda x: x.split('-')[-1] if '-' in x else x)  # sort by callsign

    if len(USER_PRIVATE_FILE) > 1:  # check for multiple private files
        print(f"Error: More than one private file found: {USER_PRIVATE_FILE}. Please resolve this issue.")
        return
    elif USER_PRIVATE_FILE:  # load user private file GUI
        mycallsign = USER_PRIVATE_FILE[0].split('/')[-1].replace('battleship-', '').replace('_private.txt', '')
        state, view_only_state, callsign = load_game_state(USER_PRIVATE_FILE[0], "private")
        create_gui(state, view_only_state, callsign, root, mycallsign)
    else:  # ask for call sign and create new user private file GUI
        mycallsign = simpledialog.askstring("Enter callsign",
                                            "No save file found. Enter your callsign to create a new one.")
        if mycallsign:
            state = [['b'] * 10 for _ in range(10)]
            view_only_state = [['b'] * 10 for _ in range(10)]
            save_private_game_state(mycallsign, state, mycallsign)
            create_gui(state, view_only_state, mycallsign, root, mycallsign)

    for file in OTHER_FILES:  # load other files GUIs
        state, view_only_state, callsign = load_game_state(file, "public")
        if state is not None:
            create_gui(state, view_only_state, callsign, root, mycallsign)

    root.mainloop()


if __name__ == "__main__":
    main()
