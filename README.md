# smart-sudoku-solver
Solve Sudoku puzzles by simulating a human approach using logic and heuristics, avoiding brute force techniques.

# smart-sudoku-solver
Solve Sudoku puzzles by simulating a human approach using logic and heuristics, avoiding brute force techniques.
# create virtual environment:
python -m venv /pat
# solve about_Execution_Policies issue on Windows
Set-ExecutionPolicy Unrestricted -Scope Process
# Activate virtualenv
.\Scripts\Activate.ps1
# Deactivate virtualenv
deactivate

Glossary:
rcs = row or column or square
square = 3v3
grid = 9x9

# Run tests:
cd src
python -m unittest discover -s ../test


# Coverage:
cd src
coverage run -m unittest discover -s ../test
coverage report -m


# Black formatting
cd src
black --config ..\pyproject.toml .