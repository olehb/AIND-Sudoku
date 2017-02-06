# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: First we identify the constraint: values which can only be assigned to a limited number of boxes. Second, we propagate this constraint by eliminating these values from all other boxes within the unit.
This procedure is then repeated for every unit in grid. My implementation generalizes Naked Twins to values longer than 2. Actually number of identical values within the unit should be equal to the length of this value.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: By adding one more channel for propagation -- diagonals, in addition to rows, columns, and 3x3 sub-grids
