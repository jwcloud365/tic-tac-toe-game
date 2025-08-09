import tkinter as tk
from tkinter import messagebox, ttk
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        
        # Modern color scheme
        self.colors = {
            'bg': '#1a1a2e',           # Dark blue background
            'card_bg': '#16213e',       # Slightly lighter for cards
            'primary': '#0f3460',       # Deep blue for buttons
            'secondary': '#533a7b',     # Purple accent
            'accent': '#f39c12',        # Orange for highlights
            'text': '#ecf0f1',          # Light gray text
            'success': '#27ae60',       # Green for X
            'danger': '#e74c3c',        # Red for O
            'hover': '#e8b923',         # Yellow for hover
        }
        
        # Configure window
        self.window.configure(bg=self.colors['bg'])
        
        # Game state
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        
        # Style configuration
        self.setup_styles()
        
        # Show starter screen with who-goes-first options
        self.show_starter_screen()
        
    def setup_styles(self):
        """Configure modern styles for the application"""
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure('Modern.TButton',
                       background=self.colors['primary'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 12, 'bold'),
                       borderwidth=2,
                       relief='flat',
                       padding=(20, 10))
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['hover']),
                           ('pressed', self.colors['secondary'])])
        
        # Configure frame style
        style.configure('Modern.TFrame',
                       background=self.colors['bg'],
                       borderwidth=0)
        
    def show_starter_screen(self):
        # Clear window if anything exists
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Main container with padding
        main_frame = tk.Frame(self.window, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Title section
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        title_frame.pack(pady=(0, 40))
        
        title_label = tk.Label(title_frame, 
                              text="TIC-TAC-TOE", 
                              font=('Segoe UI', 32, 'bold'),
                              bg=self.colors['bg'],
                              fg=self.colors['accent'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="A modern take on the classic game",
                                 font=('Segoe UI', 12),
                                 bg=self.colors['bg'],
                                 fg=self.colors['text'])
        subtitle_label.pack(pady=(10, 0))
        
        # Card container for selection
        card_frame = tk.Frame(main_frame, 
                             bg=self.colors['card_bg'],
                             relief='solid',
                             borderwidth=1)
        card_frame.pack(pady=20, padx=20, fill='x')
        
        # Card content
        card_content = tk.Frame(card_frame, bg=self.colors['card_bg'])
        card_content.pack(padx=30, pady=30)
        
        # Selection label
        label = tk.Label(card_content, 
                        text="Who should make the first move?", 
                        font=('Segoe UI', 16, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text'])
        label.pack(pady=(0, 30))
        
        # Button container
        button_frame = tk.Frame(card_content, bg=self.colors['card_bg'])
        button_frame.pack()
        
        # User starts button
        user_button = tk.Button(button_frame, 
                               text="🎮 PLAYER",
                               font=('Segoe UI', 14, 'bold'),
                               bg=self.colors['success'],
                               fg='white',
                               activebackground=self.colors['hover'],
                               activeforeground='white',
                               relief='flat',
                               borderwidth=0,
                               padx=30,
                               pady=15,
                               cursor='hand2',
                               command=lambda: self.setup_game(True))
        user_button.pack(side=tk.LEFT, padx=10)
        
        # Computer starts button
        comp_button = tk.Button(button_frame, 
                               text="🤖 COMPUTER",
                               font=('Segoe UI', 14, 'bold'),
                               bg=self.colors['danger'],
                               fg='white',
                               activebackground=self.colors['hover'],
                               activeforeground='white',
                               relief='flat',
                               borderwidth=0,
                               padx=30,
                               pady=15,
                               cursor='hand2',
                               command=lambda: self.setup_game(False))
        comp_button.pack(side=tk.LEFT, padx=10)
        
        # Add hover effects
        self.add_button_hover_effect(user_button, self.colors['success'], self.colors['hover'])
        self.add_button_hover_effect(comp_button, self.colors['danger'], self.colors['hover'])
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        footer_frame.pack(side='bottom', pady=(40, 0))
        
        footer_label = tk.Label(footer_frame,
                               text="Choose your starting preference and enjoy the game!",
                               font=('Segoe UI', 10),
                               bg=self.colors['bg'],
                               fg=self.colors['text'])
        footer_label.pack()
    
    def add_button_hover_effect(self, button, normal_color, hover_color):
        """Add hover effects to buttons"""
        def on_enter(e):
            button.configure(bg=hover_color)
        
        def on_leave(e):
            button.configure(bg=normal_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def setup_game(self, user_starts):
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.window, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section
        header_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        header_frame.pack(pady=(0, 30))
        
        title_label = tk.Label(header_frame,
                              text="TIC-TAC-TOE",
                              font=('Segoe UI', 24, 'bold'),
                              bg=self.colors['bg'],
                              fg=self.colors['accent'])
        title_label.pack()
        
        # Game info
        self.info_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        self.info_frame.pack(pady=(15, 0))
        
        self.current_player_label = tk.Label(self.info_frame,
                                           text=f"Current Player: {'🎮 Player' if self.current_player == 'X' else '🤖 Computer'}",
                                           font=('Segoe UI', 14, 'bold'),
                                           bg=self.colors['bg'],
                                           fg=self.colors['text'])
        self.current_player_label.pack()
        
        # Game board container
        board_container = tk.Frame(main_frame, bg=self.colors['bg'])
        board_container.pack(expand=True)
        
        # Create game board frame with border
        board_frame = tk.Frame(board_container, 
                              bg=self.colors['card_bg'],
                              relief='solid',
                              borderwidth=2)
        board_frame.pack(pady=20)
        
        # Create buttons with modern styling
        self.buttons = []
        for i in range(9):
            button = tk.Button(board_frame,
                              text=" ",
                              font=('Segoe UI', 32, 'bold'),
                              width=4,
                              height=2,
                              bg=self.colors['primary'],
                              fg=self.colors['text'],
                              activebackground=self.colors['hover'],
                              activeforeground='white',
                              relief='flat',
                              borderwidth=2,
                              cursor='hand2',
                              command=lambda idx=i: self.make_move(idx))
            self.buttons.append(button)
        
        # Create board layout
        self.create_board()
        
        # Control buttons
        control_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        control_frame.pack(pady=(30, 0))
        
        # New game button
        new_game_btn = tk.Button(control_frame,
                                text="🔄 NEW GAME",
                                font=('Segoe UI', 12, 'bold'),
                                bg=self.colors['secondary'],
                                fg='white',
                                activebackground=self.colors['hover'],
                                activeforeground='white',
                                relief='flat',
                                borderwidth=0,
                                padx=20,
                                pady=10,
                                cursor='hand2',
                                command=self.show_starter_screen)
        new_game_btn.pack(side=tk.LEFT, padx=5)
        
        # Add hover effect to new game button
        self.add_button_hover_effect(new_game_btn, self.colors['secondary'], self.colors['hover'])
        
        # Reset the game state
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        
        # If computer starts, make the first move
        if not user_starts:
            self.current_player = "O"
            self.window.after(500, self.computer_move)  # Small delay for better UX

    def create_board(self):
        # Create 3x3 grid with proper spacing
        for i, button in enumerate(self.buttons):
            row, col = divmod(i, 3)
            button.grid(row=row, column=col, padx=2, pady=2)
            
            # Add hover effects to game buttons
            self.add_game_button_hover_effect(button)
    
    def add_game_button_hover_effect(self, button):
        """Add hover effects to game board buttons"""
        def on_enter(e):
            if button['text'] == " ":  # Only hover empty buttons
                button.configure(bg=self.colors['hover'], borderwidth=3)
        
        def on_leave(e):
            if button['text'] == " ":  # Only reset empty buttons
                button.configure(bg=self.colors['primary'], borderwidth=2)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def update_current_player_display(self):
        """Update the current player display"""
        if hasattr(self, 'current_player_label'):
            player_text = "🎮 Player (X)" if self.current_player == "X" else "🤖 Computer (O)"
            self.current_player_label.config(text=f"Current Turn: {player_text}")

    def make_move(self, index):
        if self.board[index] == " " and self.current_player == "X":
            self.board[index] = "X"
            self.buttons[index].config(text="X", 
                                     fg=self.colors['success'],
                                     bg=self.colors['card_bg'],
                                     borderwidth=1)
            
            # Remove hover effects from played button
            self.buttons[index].unbind("<Enter>")
            self.buttons[index].unbind("<Leave>")
            
            if self.check_winner("X"):
                self.highlight_winning_combination("X")
                self.window.after(1000, lambda: self.show_game_over("🎉 You Win!", True))
            elif " " not in self.board:
                self.window.after(1000, lambda: self.show_game_over("🤝 It's a Tie!", False))
            else:
                self.current_player = "O"
                self.update_current_player_display()
                self.window.after(500, self.computer_move)

    def computer_move(self):
        # Use minimax algorithm to find the best move
        index = self.get_best_move()
        
        # If no move found (shouldn't happen), fall back to any available spot
        if index is None:
            empty_indices = [i for i, spot in enumerate(self.board) if spot == " "]
            if empty_indices:
                index = random.choice(empty_indices)
            else:
                return  # No moves available
                
        self.board[index] = "O"
        self.buttons[index].config(text="O", 
                                 fg=self.colors['danger'],
                                 bg=self.colors['card_bg'],
                                 borderwidth=1)
        
        # Remove hover effects from played button
        self.buttons[index].unbind("<Enter>")
        self.buttons[index].unbind("<Leave>")
        
        if self.check_winner("O"):
            self.highlight_winning_combination("O")
            self.window.after(1000, lambda: self.show_game_over("🤖 Computer Wins!", False))
        elif " " not in self.board:
            self.window.after(1000, lambda: self.show_game_over("🤝 It's a Tie!", False))
        else:
            self.current_player = "X"
            self.update_current_player_display()
    
    def highlight_winning_combination(self, player):
        """Highlight the winning combination"""
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                for i in condition:
                    self.buttons[i].config(bg=self.colors['accent'], 
                                         fg='white',
                                         borderwidth=3)
                break
    
    def show_game_over(self, message, player_won):
        """Show modern game over dialog"""
        # Create overlay
        overlay = tk.Toplevel(self.window)
        overlay.title("Game Over")
        overlay.geometry("400x250")
        overlay.configure(bg=self.colors['bg'])
        overlay.resizable(False, False)
        overlay.grab_set()  # Make it modal
        
        # Center the window
        overlay.transient(self.window)
        
        # Main frame
        main_frame = tk.Frame(overlay, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Message
        msg_label = tk.Label(main_frame,
                           text=message,
                           font=('Segoe UI', 18, 'bold'),
                           bg=self.colors['bg'],
                           fg=self.colors['accent'])
        msg_label.pack(pady=(20, 30))
        
        # Buttons frame
        btn_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=20)
        
        # Play again button
        play_again_btn = tk.Button(btn_frame,
                                 text="🎮 PLAY AGAIN",
                                 font=('Segoe UI', 12, 'bold'),
                                 bg=self.colors['success'],
                                 fg='white',
                                 activebackground=self.colors['hover'],
                                 activeforeground='white',
                                 relief='flat',
                                 borderwidth=0,
                                 padx=20,
                                 pady=10,
                                 cursor='hand2',
                                 command=lambda: [overlay.destroy(), self.show_starter_screen()])
        play_again_btn.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        quit_btn = tk.Button(btn_frame,
                           text="❌ QUIT",
                           font=('Segoe UI', 12, 'bold'),
                           bg=self.colors['danger'],
                           fg='white',
                           activebackground=self.colors['hover'],
                           activeforeground='white',
                           relief='flat',
                           borderwidth=0,
                           padx=20,
                           pady=10,
                           cursor='hand2',
                           command=self.window.quit)
        quit_btn.pack(side=tk.LEFT, padx=10)
        
        # Add hover effects
        self.add_button_hover_effect(play_again_btn, self.colors['success'], self.colors['hover'])
        self.add_button_hover_effect(quit_btn, self.colors['danger'], self.colors['hover'])
            
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
    
    def is_terminal_state(self):
        """Check if the game has ended (win or tie)"""
        return self.check_winner("X") or self.check_winner("O") or " " not in self.board
    
    def evaluate_board(self):
        """Evaluate the current board state for minimax
        Returns: 1 if computer wins, -1 if player wins, 0 if tie"""
        if self.check_winner("O"):  # Computer wins
            return 1
        elif self.check_winner("X"):  # Player wins
            return -1
        else:  # Tie or game not over
            return 0
    
    def minimax(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        """Minimax algorithm implementation with alpha-beta pruning
        Args:
            depth: Current depth in the game tree
            is_maximizing: True if maximizing player's turn (computer), False otherwise
            alpha: Best value that maximizer can guarantee
            beta: Best value that minimizer can guarantee
        Returns:
            Best score for the current position
        """
        # Base case: if game is over, return the evaluation
        if self.is_terminal_state():
            return self.evaluate_board()
        
        if is_maximizing:  # Computer's turn (maximize score)
            max_eval = float('-inf')
            for i in range(9):
                if self.board[i] == " ":
                    # Make the move
                    self.board[i] = "O"
                    # Recursively evaluate
                    eval_score = self.minimax(depth + 1, False, alpha, beta)
                    # Undo the move
                    self.board[i] = " "
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break  # Alpha-beta pruning
            return max_eval
        else:  # Player's turn (minimize score)
            min_eval = float('inf')
            for i in range(9):
                if self.board[i] == " ":
                    # Make the move
                    self.board[i] = "X"
                    # Recursively evaluate
                    eval_score = self.minimax(depth + 1, True, alpha, beta)
                    # Undo the move
                    self.board[i] = " "
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break  # Alpha-beta pruning
            return min_eval
    
    def get_best_move(self):
        """Find the best move using minimax algorithm
        Returns: Best move index, or None if no moves available
        """
        best_move = None
        best_score = float('-inf')
        
        for i in range(9):
            if self.board[i] == " ":
                # Make the move
                self.board[i] = "O"
                # Evaluate the move
                score = self.minimax(0, False)
                # Undo the move
                self.board[i] = " "
                
                # Update best move if this is better
                if score > best_score:
                    best_score = score
                    best_move = i
        
        return best_move

if __name__ == "__main__":
    game = TicTacToe()
    game.window.mainloop()  # Move mainloop to the end