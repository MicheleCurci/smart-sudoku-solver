# smart-sudoku-solver
Solve Sudoku puzzles by simulating a human approach using logic and heuristics, avoiding brute force techniques.

Glossary:
rcs = row or column or square
square = 3v3
grid = 9x9

# create virtual environment:
python -m venv /pat

# solve about_Execution_Policies issue on Windows
Set-ExecutionPolicy Unrestricted -Scope Process

# Activate virtualenv
.\Scripts\Activate.ps1

# Deactivate virtualenv
deactivate

# Run tests:
python -m unittest

# Coverage:
coverage run -m unittest
coverage report -m

# Black formatting
black --config pyproject.toml src tests