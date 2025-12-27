"""
Fichier de test - Person 1
"""
from sat import *

# Test manuel
formule_test = [
    [1, 2, 3],
    [-1, -2],
    [2, -3]
]
vars_test = [1, 2, 3]

print("Test en cours...")
sol = solve_sat_bruteforce(formule_test, vars_test)
print(f"Solution: {sol}")