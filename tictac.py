import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        
        # Show starter screen with who-goes-first options
        self.show_starter_screen()
        
    def show_starter_screen(self):
        # Clear window if anything exists
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Create frame for selection
        frame = tk.Frame(self.window)
        frame.pack(pady=20)
        
        # Add label
        label = tk.Label(frame, text="Who should make the first move?", font=("Arial", 14))
        label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        # User starts button
        user_button = tk.Button(button_frame, text="User", width=10, font=("Arial", 12),
                              command=lambda: self.setup_game(True))
        user_button.pack(side=tk.LEFT, padx=10)
        
        # Computer starts button
        comp_button = tk.Button(button_frame, text="Computer", width=10, font=("Arial", 12),
                              command=lambda: self.setup_game(False))
        comp_button.pack(side=tk.LEFT, padx=10)
    
    def setup_game(self, user_starts):
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Create buttons
        self.buttons = [tk.Button(self.window, text=" ", font=("Arial", 24), height=2, width=5,
                                command=lambda i=i: self.make_move(i)) for i in range(9)]
        
        # Create board
        self.create_board()
        
        # Reset the game state
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        
        # If computer starts, make the first move
        if not user_starts:
            self.current_player = "O"
            self.computer_move()

    def create_board(self):
        for i, button in enumerate(self.buttons):
            row, col = divmod(i, 3)
            button.grid(row=row, column=col)

    def make_move(self, index):
        if self.board[index] == " " and self.current_player == "X":
            self.board[index] = "X"
            self.buttons[index].config(text="X")
            if self.check_winner("X"):
                messagebox.showinfo("Game Over", "You win!")
                self.show_starter_screen()  # Return to starter screen instead of just resetting
            elif " " not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.show_starter_screen()  # Return to starter screen instead of just resetting
            else:
                self.current_player = "O"
                self.computer_move()

    def computer_move(self):
        # Try to win
        move = self.find_winning_move("O")
        if move is not None:
            index = move
        # Block player's winning move
        elif (block_move := self.find_winning_move("X")) is not None:
            index = block_move
        # Take center if available
        elif self.board[4] == " ":
            index = 4
        # Take a corner if available
        elif any(self.board[i] == " " for i in [0, 2, 6, 8]):
            corners = [i for i in [0, 2, 6, 8] if self.board[i] == " "]
            index = random.choice(corners)
        # Take any available spot
        else:
            empty_indices = [i for i, spot in enumerate(self.board) if spot == " "]
            if empty_indices:  # Check if there are any empty spots
                index = random.choice(empty_indices)
            else:
                return  # No moves available
            
        self.board[index] = "O"
        self.buttons[index].config(text="O")
        if self.check_winner("O"):
            messagebox.showinfo("Game Over", "Computer wins!")
            self.show_starter_screen()  # Return to starter screen instead of just resetting
        elif " " not in self.board:
            messagebox.showinfo("Game Over", "It's a tie!")
            self.show_starter_screen()  # Return to starter screen instead of just resetting
        else:
            self.current_player = "X"
            
    def find_winning_move(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for condition in win_conditions:
            values = [self.board[i] for i in condition]
            if values.count(player) == 2 and values.count(" ") == 1:
                return condition[values.index(" ")]
        return None

    def check_winner(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        return any(all(self.board[i] == player for i in condition) for condition in win_conditions)

if __name__ == "__main__":
    game = TicTacToe()
    game.window.mainloop()  # Move mainloop to the end