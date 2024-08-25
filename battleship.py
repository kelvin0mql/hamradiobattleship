import tkinter as tk
from tkinter import messagebox
import os
import glob
from pathlib import Path


def load_game_state(fname):
    home = str(Path.home())
    filepath = os.path.join(home, fname)

    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()
        state = [list(line.strip()) for line in lines]
    else:
        state = [['b'] * 10 for _ in range(10)]

    return state, fname.replace(".txt", "").replace("battleship-", "")


def save_game_state(callsign, state):
    home = str(Path.home())
    filename = f'battleship-{callsign}.txt'
    filepath = os.path.join(home, filename)
    with open(filepath, 'w') as file:
        for row in state:
            file.write(''.join(row) + '\n')


def reset_grid(grid, state, callsign):
    confirmed = messagebox.askokcancel(title='Confirmation',
                                       message='Are you sure you want to clear the entire grid?')
    if confirmed:
        for i in range(10):
            for j in range(10):
                state[i][j] = 'b'
                grid[i][j].configure(bg='light blue')
        save_game_state(callsign, state)


def create_gui(state, callsign, root):
    frame = tk.Frame(root)
    frame.pack(side="left", padx=5, pady=5)
    grid_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    # Add labels to the top of the grid
    for j in range(10):
        tk.Label(frame, text=str(j + 1)).grid(row=0, column=j + 1)

    # Add labels to left of the grid.
    for i in range(10):
        tk.Label(frame, text=grid_labels[i]).grid(row=i + 1, column=0)

    def on_click(i, j, label, callsign, state):
        if state[i][j] == 'b':
            state[i][j] = 'm'
            label.configure(bg='white')
        elif state[i][j] == 'm':
            state[i][j] = 'r'
            label.configure(bg='red')
        elif state[i][j] == 'r':
            state[i][j] = 'h'
            label.configure(bg='black')
        elif state[i][j] == 'h':
            state[i][j] = 'b'
            label.configure(bg='light blue')

        save_game_state(callsign, state)

    grid = []
    for i in range(10):
        row = []
        for j in range(10):
            color = 'light blue'
            if state[i][j] == 'm':
                color = 'white'
            elif state[i][j] == 'h':
                color = 'black'
            elif state[i][j] == 'r':
                color = 'red'
            elif state[i][j] == 's':
                color = 'black'
            label = tk.Label(frame, width=2, height=1, bg=color)
            label.grid(row=i + 1, column=j + 1, padx=1, pady=1)
            label.bind('<Button-1>',
                       lambda event, i=i, j=j, label=label, callsign=callsign, state=state: on_click(i, j, label,
                                                                                                     callsign, state))
            row.append(label)
        grid.append(row)

    reset_button = tk.Button(frame, text=f"Reset {callsign}", command=lambda: reset_grid(grid, state, callsign))
    reset_button.grid(row=12, column=1, columnspan=10, sticky="nsew")


def main():
    home = str(Path.home())
    battleship_files = [os.path.basename(x) for x in glob.glob(home + "/battleship-*.txt")]

    root = tk.Tk()
    root.title("Battleship Game")

    for file in battleship_files:
        state, callsign = load_game_state(file)
        create_gui(state, callsign, root)

    root.mainloop()


main()
