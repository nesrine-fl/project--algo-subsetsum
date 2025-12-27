from read_write_files import write_subsetsum_instance

def sat_to_subsetsum_base2(clauses, num_vars):
    m = len(clauses)
    base = 4
    width = num_vars + m
    
    numbers = []
    meta = {"var_pos": {}, "clause_fillers": [[] for _ in range(m)]}
    
    def make_number(digits):
        value = 0
        for d in digits:
            value = value * base + d
        return value
    
    for i in range(1, num_vars + 1):
        for sign in [True, False]:
            digits = [0] * width
            digits[i - 1] = 1 
            for j, clause in enumerate(clauses):
                lit = i if sign else -i
                if lit in clause:
                    digits[num_vars + j] = 1 
            number = make_number(digits)
            meta["var_pos"][(i, sign)] = len(numbers)
            numbers.append(number)
    
    # Clause filler numbers
    for j in range(m):
        digits = [0] * width
        digits[num_vars + j] = 1
        # add 3 fillers per clause, but we'll pick dynamically later
        for _ in range(3):
            meta["clause_fillers"][j].append(len(numbers))
            numbers.append(make_number(digits))
    
    # Target digits: variable columns = 1, clause columns = 3
    target_digits = [1]*num_vars + [3]*m
    target = make_number(target_digits)
    
    return numbers, target, meta


def sat_solution_to_subset(assignment, numbers, meta, clauses):
    subset = []
    
    # pick exactly one literal per variable
    for var, value in assignment.items():
        idx = meta["var_pos"][(var, value)]
        subset.append(numbers[idx])
    
    # add clause fillers carefully
    for j, clause in enumerate(clauses):
        # check which literals in clause are True
        true_literals = sum(
            1 for lit in clause if (lit > 0 and assignment.get(lit, False)) 
                                  or (lit < 0 and not assignment.get(-lit, False))
        )
        if true_literals == 0:
            # clause is not satisfied, cannot reach target
            continue  # do NOT add any fillers
        # add exactly enough fillers to reach target
        num_fillers_needed = 3 - true_literals
        subset += [numbers[idx] for idx in meta["clause_fillers"][j][:num_fillers_needed]]
    
    return subset

def subset_to_binary_solution(subset, weights):
    """
    Convert a chosen subset (list of numbers) into a binary vector over weights.
    Works even if weights have duplicates.
    """
    subset_copy = subset[:]
    solution = []

    for w in weights:
        if w in subset_copy:
            solution.append(1)
            subset_copy.remove(w)
        else:
            solution.append(0)

    return solution
