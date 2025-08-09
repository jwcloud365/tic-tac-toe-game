#!/usr/bin/env python3
"""
Basic import test for Tic-Tac-Toe game.
Note: This is a minimal test. Use test_game_logic.py for comprehensive testing.
"""

def test_basic_import():
    """Test that the main module can be imported without errors."""
    try:
        # Import the main module without initializing the GUI
        # This tests for syntax errors and import issues
        import sys
        import os
        
        # Add current directory to path to import tictac module
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Import the module - this will fail if there are syntax errors
        import tictac
        
        # Check that the main class exists
        assert hasattr(tictac, 'TicTacToe'), "TicTacToe class not found"
        
        print("✓ Basic import test passed")
        return True
        
    except Exception as e:
        print(f"✗ Basic import test failed: {e}")
        return False

if __name__ == "__main__":
    test_basic_import()