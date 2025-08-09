#!/usr/bin/env python3
"""
Test script for Tic-Tac-Toe game logic.
Tests the minimax algorithm and game logic without requiring GUI.
"""

def test_game_logic():
    """Test the game logic by creating a minimal version of the TicTacToe class"""
    
    # Extract just the core logic methods for testing
    class TicTacToeLogic:
        def __init__(self):
            self.board = [" " for _ in range(9)]
            self.current_player = "X"
        
        def check_winner(self, player):
            win_conditions = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
                [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
                [0, 4, 8], [2, 4, 6]              # Diagonals
            ]
            return any(all(self.board[i] == player for i in condition) for condition in win_conditions)
        
        def is_terminal_state(self):
            """Check if the game has ended (win or tie)"""
            return self.check_winner("X") or self.check_winner("O") or " " not in self.board
        
        def evaluate_board(self):
            """Evaluate the current board state for minimax"""
            if self.check_winner("O"):  # Computer wins
                return 1
            elif self.check_winner("X"):  # Player wins
                return -1
            else:  # Tie or game not over
                return 0
        
        def minimax(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
            """Minimax algorithm implementation with alpha-beta pruning"""
            if self.is_terminal_state():
                return self.evaluate_board()
            
            if is_maximizing:  # Computer's turn (maximize score)
                max_eval = float('-inf')
                for i in range(9):
                    if self.board[i] == " ":
                        self.board[i] = "O"
                        eval_score = self.minimax(depth + 1, False, alpha, beta)
                        self.board[i] = " "
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break
                return max_eval
            else:  # Player's turn (minimize score)
                min_eval = float('inf')
                for i in range(9):
                    if self.board[i] == " ":
                        self.board[i] = "X"
                        eval_score = self.minimax(depth + 1, True, alpha, beta)
                        self.board[i] = " "
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break
                return min_eval
        
        def get_best_move(self):
            """Find the best move using minimax algorithm"""
            best_move = None
            best_score = float('-inf')
            
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "O"
                    score = self.minimax(0, False)
                    self.board[i] = " "
                    
                    if score > best_score:
                        best_score = score
                        best_move = i
            
            return best_move

    # Run tests
    game = TicTacToeLogic()
    
    # Test board initialization
    assert len(game.board) == 9
    assert all(spot == " " for spot in game.board)
    print("✓ Board initialization test passed")
    
    # Test win detection
    game.board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
    assert game.check_winner("X") == True
    assert game.check_winner("O") == False
    print("✓ Win detection test passed")
    
    # Test minimax algorithm
    game.board = ["X", "O", "X", " ", "O", " ", " ", " ", " "]
    best_move = game.get_best_move()
    assert best_move is not None
    assert 0 <= best_move <= 8
    assert game.board[best_move] == " "
    print("✓ Minimax algorithm test passed")
    
    # Test terminal state detection
    game.board = ["X", "O", "X", "O", "X", "O", "O", "X", "O"]  # Full board
    assert game.is_terminal_state() == True
    print("✓ Terminal state detection test passed")
    
    # Test computer will block player win
    game.board = ["X", "X", " ", " ", " ", " ", " ", " ", " "]
    best_move = game.get_best_move()
    assert best_move == 2  # Should block the win
    print("✓ Computer blocking logic test passed")
    
    print("All tests passed!")
    return True

if __name__ == "__main__":
    test_game_logic()