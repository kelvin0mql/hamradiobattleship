import tkinter as tk
from tkinter import messagebox
import os
import glob
from pathlib import Path


def load_game_state(callsign=None):
    home = str(Path.home())
    battleship_files = glob.glob(home + "/battleship-*.txt")
    if battleship_files:
        filename = os.path.basename(battleship_files[0])
        callsign = filename.replace("battleship-", "").replace(".txt", "")
    elif callsign is None:
        callsign = input("Enter your callsign: ")

    filename = f'battleship-{callsign}.txt'

    filepath = os.path.join(home, filename)
    if not os.path.exists(filepath):
        return [['b'] * 10 for _ in range(10)], callsign
    with open(filepath, 'r') as file:
        lines = file.readlines()
    state = [list(line.strip()) for line in lines]
    return state, callsign


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


def create_gui(state, callsign):
    root = tk.Tk()
    root.title("Battleship Game")

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
            label = tk.Label(root, width=2, height=1, bg=color)
            label.grid(row=i, column=j, padx=1, pady=1)
            label.bind('<Button-1>',
                       lambda event, i=i, j=j, label=label, callsign=callsign, state=state: on_click(i, j, label,
                                                                                                     callsign, state))
            row.append(label)
        grid.append(row)

    reset_button = tk.Button(root, text="Reset", command=lambda: reset_grid(grid, state, callsign))
    reset_button.grid(row=11, column=0, columnspan=10)

    root.mainloop()


def main():
    state, callsign = load_game_state()
    create_gui(state, callsign)
    save_game_state(callsign, state)


main()
