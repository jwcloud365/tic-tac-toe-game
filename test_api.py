#!/usr/bin/env python
"""
Test TicTacToe API

This script tests the Tic-Tac-Toe game API endpoints to verify that
the application is working correctly.
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional

class TicTacToeAPITester:
    """Tests the Tic-Tac-Toe game API endpoints."""
    
    def __init__(self, base_url: str) -> None:
        """
        Initialize with the base URL of the API.
        
        Args:
            base_url: The base URL of the API (e.g., http://localhost:5000 or https://example.azurewebsites.net)
        """
        self.base_url = base_url.rstrip('/')
        self.tests_passed = 0
        self.tests_failed = 0
        
    def run_tests(self) -> None:
        """Run all API tests."""
        self.print_header(f"Testing Tic-Tac-Toe API at {self.base_url}")
        
        # Test homepage
        self.test_homepage()
        
        # Test reset endpoint
        game_state = self.test_reset_game("X")
        if not game_state:
            self.print_error("Failed to reset game, skipping further tests")
            self.print_summary()
            return
        
        # Test player move
        game_state = self.test_player_move(0, game_state)
        if not game_state:
            self.print_error("Failed to make player move, skipping further tests")
            self.print_summary()
            return
        
        # Test game winning conditions
        self.test_winning_sequence()
        
        # Test game tie conditions
        self.test_tie_sequence()
        
        # Test computer starting first
        self.test_computer_starts()
        
        # Print summary of tests
        self.print_summary()
    
    def test_homepage(self) -> bool:
        """Test that the homepage loads correctly."""
        self.print_test_header("Testing homepage")
        
        try:
            # Request the homepage
            response = urllib.request.urlopen(f"{self.base_url}/")
            content = response.read().decode('utf-8')
            
            # Check status code
            self.assert_test(response.getcode() == 200, "Homepage returns 200 OK")
            
            # Check content
            self.assert_test("Tic-Tac-Toe" in content, "Homepage contains 'Tic-Tac-Toe' title")
            self.assert_test("<div class=\"board\"" in content, "Homepage contains game board")
            
            return True
        except Exception as e:
            self.assert_test(False, f"Homepage request failed: {str(e)}")
            return False
    
    def test_reset_game(self, first_player: str) -> Optional[Dict[str, Any]]:
        """
        Test the reset endpoint.
        
        Args:
            first_player: Which player goes first ("X" for user, "O" for computer)
            
        Returns:
            Game state dict or None if test failed
        """
        self.print_test_header(f"Testing reset game with {first_player} going first")
        
        try:
            # Call reset endpoint
            headers = {'Content-Type': 'application/json'}
            data = json.dumps({"firstPlayer": first_player}).encode('utf-8')
            req = urllib.request.Request(
                f"{self.base_url}/reset", 
                data=data, 
                headers=headers, 
                method='POST'
            )
            response = urllib.request.urlopen(req)
            game_state = json.loads(response.read().decode('utf-8'))
            
            # Check response
            self.assert_test(response.getcode() == 200, "Reset returns 200 OK")
            self.assert_test("board" in game_state, "Response contains board")
            self.assert_test("currentPlayer" in game_state, "Response contains currentPlayer")
            self.assert_test("gameOver" in game_state, "Response contains gameOver")
            
            # Check board is empty
            if "board" in game_state:
                empty_cells = [cell for cell in game_state["board"] if cell == " "]
                self.assert_test(len(empty_cells) == 9, "Board is empty")
            
            # Check player is set correctly
            if "currentPlayer" in game_state:
                self.assert_test(game_state["currentPlayer"] == first_player, f"Current player is {first_player}")
            
            # When computer starts first, it should make a move
            if first_player == "O" and "board" in game_state:
                computer_moves = [cell for cell in game_state["board"] if cell == "O"]
                self.assert_test(len(computer_moves) == 1, "Computer made first move")
            
            return game_state
        except Exception as e:
            self.assert_test(False, f"Reset game failed: {str(e)}")
            return None
    
    def test_player_move(self, index: int, previous_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Test making a player move.
        
        Args:
            index: Board position (0-8)
            previous_state: Previous game state
            
        Returns:
            Updated game state or None if test failed
        """
        self.print_test_header(f"Testing player move at position {index}")
        
        try:
            # Call move endpoint
            headers = {'Content-Type': 'application/json'}
            data = json.dumps({"index": index}).encode('utf-8')
            req = urllib.request.Request(
                f"{self.base_url}/move", 
                data=data, 
                headers=headers, 
                method='POST'
            )
            response = urllib.request.urlopen(req)
            game_state = json.loads(response.read().decode('utf-8'))
            
            # Check response
            self.assert_test(response.getcode() == 200, "Move returns 200 OK")
            self.assert_test("board" in game_state, "Response contains board")
            
            # Check player move recorded
            if "board" in game_state:
                self.assert_test(game_state["board"][index] == "X", f"Position {index} marked as X")
            
            # Check computer made a counter move
            if "board" in game_state:
                o_count_before = sum(1 for cell in previous_state["board"] if cell == "O")
                o_count_after = sum(1 for cell in game_state["board"] if cell == "O")
                self.assert_test(o_count_after == o_count_before + 1, "Computer made a counter move")
            
            # Check computerMove in response
            self.assert_test("computerMove" in game_state, "Response contains computerMove")
            
            return game_state
        except Exception as e:
            self.assert_test(False, f"Player move failed: {str(e)}")
            return None
    
    def test_winning_sequence(self) -> None:
        """Test a winning sequence for the player."""
        self.print_test_header("Testing player winning sequence")
        
        try:
            # Reset game
            game_state = self.test_reset_game("X")
            if not game_state:
                return
            
            # Create a winning sequence for X (top row)
            # Player: top-left (0)
            game_state = self.make_move(0)
            if not game_state:
                return
            
            # Player: top-middle (1)
            game_state = self.make_move(1)
            if not game_state:
                return
            
            # Player: top-right (2)
            game_state = self.make_move(2)
            
            # Verify player won
            self.assert_test(game_state.get("winner") == "X", "Player X wins the game")
            self.assert_test(game_state.get("gameOver") == True, "Game is over")
            
        except Exception as e:
            self.assert_test(False, f"Winning sequence test failed: {str(e)}")
    
    def test_tie_sequence(self) -> None:
        """Test a game ending in a tie."""
        self.print_test_header("Testing tie game sequence")
        
        try:
            # This is a predictable sequence that should lead to a tie
            # if the computer plays optimally
            game_state = self.test_reset_game("X")
            
            # Player takes center
            game_state = self.make_move(4)
            
            # Computer should take a corner (0, 2, 6, or 8)
            # Player takes opposite corner
            corner_map = {0: 8, 2: 6, 6: 2, 8: 0}
            computer_move = game_state.get("computerMove")
            if computer_move in corner_map:
                game_state = self.make_move(corner_map[computer_move])
            else:
                # If computer didn't take corner, just continue with a sequence
                game_state = self.make_move(0)
            
            # Continue making moves until game is over
            positions = [1, 3, 5, 7]
            for pos in positions:
                if not game_state.get("gameOver"):
                    game_state = self.make_move(pos)
                    if not game_state:
                        return
            
            # Check if game ended in a tie or someone won
            if game_state.get("winner") is None and game_state.get("gameOver"):
                self.assert_test(True, "Game ended in a tie")
            else:
                self.assert_test(game_state.get("gameOver"), "Game is over")
            
        except Exception as e:
            self.assert_test(False, f"Tie sequence test failed: {str(e)}")
    
    def test_computer_starts(self) -> None:
        """Test a game where computer starts first."""
        self.print_test_header("Testing computer starting first")
        
        try:
            # Reset game with computer first
            game_state = self.test_reset_game("O")
            if not game_state:
                return
            
            # Verify computer made first move
            o_count = sum(1 for cell in game_state["board"] if cell == "O")
            self.assert_test(o_count == 1, "Computer made the first move")
            self.assert_test(game_state["currentPlayer"] == "X", "Current player switched to X")
            
            # Make a player move
            index = game_state["board"].index(" ")  # Find first empty cell
            game_state = self.make_move(index)
            
            # Verify another computer move
            o_count = sum(1 for cell in game_state["board"] if cell == "O")
            self.assert_test(o_count == 2, "Computer made a second move")
            
        except Exception as e:
            self.assert_test(False, f"Computer starts test failed: {str(e)}")
    
    def make_move(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Helper to make a move and return the updated state.
        
        Args:
            index: Board position (0-8)
            
        Returns:
            Updated game state or None if failed
        """
        try:
            headers = {'Content-Type': 'application/json'}
            data = json.dumps({"index": index}).encode('utf-8')
            req = urllib.request.Request(
                f"{self.base_url}/move", 
                data=data, 
                headers=headers, 
                method='POST'
            )
            response = urllib.request.urlopen(req)
            return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            self.assert_test(False, f"Move to position {index} failed: {str(e)}")
            return None
    
    def assert_test(self, condition: bool, message: str) -> None:
        """
        Assert a test condition and update test counts.
        
        Args:
            condition: Test condition to check
            message: Test message to display
        """
        if condition:
            print(f"  ✅ {message}")
            self.tests_passed += 1
        else:
            print(f"  ❌ {message}")
            self.tests_failed += 1
    
    def print_header(self, title: str) -> None:
        """Print a section header."""
        border = "=" * (len(title) + 4)
        print(f"\n{border}")
        print(f"  {title}  ")
        print(f"{border}\n")
    
    def print_test_header(self, title: str) -> None:
        """Print a test section header."""
        print(f"\n>> {title}:")
    
    def print_error(self, message: str) -> None:
        """Print an error message."""
        print(f"\n❌ ERROR: {message}")
    
    def print_summary(self) -> None:
        """Print test summary."""
        total = self.tests_passed + self.tests_failed
        self.print_header("Test Summary")
        print(f"Total tests:  {total}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_failed}")
        
        if self.tests_failed == 0:
            print("\n✅ All tests passed! The Tic-Tac-Toe API is working correctly.")
        else:
            print(f"\n❌ {self.tests_failed} tests failed. See the output above for details.")

def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test the Tic-Tac-Toe game API")
    parser.add_argument("--url", default="http://localhost:5000", 
                        help="Base URL of the Tic-Tac-Toe API (default: http://localhost:5000)")
    
    args = parser.parse_args()
    
    tester = TicTacToeAPITester(args.url)
    tester.run_tests()

if __name__ == "__main__":
    main()
