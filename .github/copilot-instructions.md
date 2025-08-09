# Tic-Tac-Toe Game

A Python-based Tic-Tac-Toe game with GUI using tkinter and minimax AI algorithm. The game features a starter screen for choosing who goes first and an intelligent computer opponent.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Quick Setup and Validation
- Install Python 3.x with tkinter:
  - `sudo apt-get update && sudo apt-get install -y python3-tk` (takes ~30-60 seconds)
- Validate syntax: `python3 -m py_compile tictac.py` (takes <1 second)
- Install dependencies: `pip install -r requirements.txt` (takes <1 second - no external dependencies)
- Run tests: `python3 test_game_logic.py` (takes <1 second)

### Building and Testing
- **CRITICAL**: There is no traditional "build" process. This is a single-file Python application.
- Syntax validation: `python3 -m py_compile tictac.py` - validates code compiles correctly
- Logic testing: `python3 test_game_logic.py` - tests minimax AI and game logic without requiring GUI
- **NEVER CANCEL**: All operations complete in under 1 second, but always set timeout to 60+ seconds for safety

### Running the Application
- **GUI Version**: `python3 tictac.py` 
  - **IMPORTANT**: Requires a display (X11/Wayland). Will fail in headless environments with "no display name and no $DISPLAY environment variable"
  - **DO NOT ATTEMPT** to run the GUI version in CI/headless environments
- **Testing Only**: Use `python3 test_game_logic.py` for validation without display requirements

### Linting and Code Quality
- Install linting: `python3 -m pip install flake8 --user` (takes ~10 seconds)
- Run linting: `python3 -m flake8 tictac.py --max-line-length=88` (takes <1 second)
- **Expected Issues**: The current code has style issues (whitespace, line length) but runs correctly
- Always run linting before commits to maintain code quality

## Validation

### Manual Testing Scenarios
- **CRITICAL**: You CANNOT test the GUI functionality in headless environments
- **Logic Testing**: Always run `python3 test_game_logic.py` after code changes to validate:
  - Board initialization and state management
  - Win condition detection for both players
  - Minimax algorithm correctness
  - Computer blocking and winning moves
  - Terminal state detection (wins/ties)

### Required Validation Steps
- Always run these commands after making changes:
  1. `python3 -m py_compile tictac.py` - syntax validation
  2. `python3 test_game_logic.py` - logic validation  
  3. `python3 -m flake8 tictac.py --max-line-length=88` - style checking

### Azure Deployment
- The `.github/github_workflows_deploy-to-azure.yml` workflow handles deployment
- **WARNING**: The deployment attempts to deploy a tkinter GUI app to Azure Web App, which may not work as intended
- The workflow expects `requirements.txt` (provided - no external dependencies needed)
- **NEVER CANCEL**: Deployment workflow should complete, but the tkinter GUI won't function in a web environment

## Common Tasks

### Repository Structure
```
.
├── .github/
│   └── github_workflows_deploy-to-azure.yml  # Azure deployment workflow
├── .gitignore                                 # Python gitignore with test exclusions
├── LICENSE                                    # MIT License
├── requirements.txt                           # Empty - no external dependencies
├── tictac.py                                 # Main game file (210 lines)
├── test_game_logic.py                        # Logic tests (works without GUI)
└── test_basic.py                             # Basic import test (not recommended)
```

### Key Files Content

#### tictac.py (Main Game)
- `TicTacToe` class with tkinter GUI
- Minimax algorithm with alpha-beta pruning
- Starter screen for choosing first player
- Game logic: win detection, move validation, AI opponent

#### test_game_logic.py (Recommended Testing)
- Tests core game logic without GUI dependencies
- Validates minimax algorithm behavior
- Checks win conditions and blocking logic
- Safe to run in any environment

#### requirements.txt
- Empty file to satisfy Azure deployment workflow
- No external Python dependencies required

### Development Workflow
1. Make code changes to `tictac.py`
2. Run syntax check: `python3 -m py_compile tictac.py`
3. Run logic tests: `python3 test_game_logic.py`
4. Run linting: `python3 -m flake8 tictac.py --max-line-length=88`
5. Commit changes (test files will be excluded by .gitignore)

### Common Issues and Solutions
- **"no display name and no $DISPLAY environment variable"**: This is expected in headless environments. Use `test_game_logic.py` instead
- **Flake8 style errors**: Code runs correctly despite style issues. Fix warnings for better code quality
- **Import errors**: Ensure tkinter is installed with `sudo apt-get install -y python3-tk`

### Performance Expectations
- All validation commands complete in under 1 second
- No long-running builds or compilation steps
- **NEVER CANCEL**: Set timeouts to 60+ seconds for safety, though operations complete quickly

### Testing Coverage
- Game initialization and board setup
- Win condition detection (rows, columns, diagonals)
- Minimax algorithm decision making
- Computer blocking player wins
- Terminal state detection (win/tie conditions)
- **NOT COVERED**: GUI interactions, visual elements, user input handling