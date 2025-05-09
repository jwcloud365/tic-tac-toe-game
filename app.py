# Web version of Tic-Tac-Toe game

from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

class TicTacToeGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.winner = None
        self.game_over = False

    def make_move(self, index):
        if self.game_over or self.board[index] != " ":
            return False
            
        self.board[index] = self.current_player
        
        # Check for winner
        if self.check_winner(self.current_player):
            self.winner = self.current_player
            self.game_over = True
            return True
            
        # Check for tie
        if " " not in self.board:
            self.game_over = True
            return True
            
        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        return True

    def computer_move(self):
        if self.game_over or self.current_player != "O":
            return False
            
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
            if empty_indices:
                index = random.choice(empty_indices)
            else:
                return False
                
        self.make_move(index)
        return index
            
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

    def get_game_state(self):
        return {
            "board": self.board,
            "currentPlayer": self.current_player,
            "winner": self.winner,
            "gameOver": self.game_over
        }

# Create a game instance
game = TicTacToeGame()

@app.route('/')
def index():
    game.reset_game()
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset():
    game.reset_game()
    first_player = request.json.get('firstPlayer', 'X')
    game.current_player = first_player
    
    response_data = game.get_game_state()
    
    # If computer goes first, make a move
    if game.current_player == "O":
        computer_move = game.computer_move()
        response_data = game.get_game_state()
        response_data["computerMove"] = computer_move
    
    return jsonify(response_data)

@app.route('/move', methods=['POST'])
def make_move():
    index = request.json.get('index')
    
    # Player move
    if game.make_move(index):
        response_data = game.get_game_state()
        
        # Computer move (if game not over and it's computer's turn)
        if not game.game_over and game.current_player == "O":
            computer_move = game.computer_move()
            response_data = game.get_game_state()
            response_data["computerMove"] = computer_move
            
        return jsonify(response_data)
    
    return jsonify({"error": "Invalid move"}), 400

if __name__ == '__main__':
    # Use environment variable for port if available (for Azure)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
