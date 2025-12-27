from read_write_files import write_dimacs
from sat import verify_sat

# SAT -> 3-SAT
def sat_3sat(clauses,aux_start=1):
    new_clauses=[]
    aux = aux_start
    for clause in clauses:
        n = len(clause)
        if n == 3:
            new_clauses.append(clause)
        elif n==1:
            y = aux
            z = aux+1
            aux+=2
            new_clauses.append([clause[0],y,z])
            new_clauses.append([clause[0],-y,z])
            new_clauses.append([clause[0],y,-z])
            new_clauses.append([clause[0],-y,-z])
        elif n==2:
            y=aux
            aux+=1
            new_clauses.append([clause[0],clause[1],y])
            new_clauses.append([clause[0],clause[1],-y])
        else:
            literals = clause[:]
            prev = literals[0]
            curr = literals[1]
            for i in range(2,n-1):
                y=aux
                new_clauses.append([prev,curr,y])
                prev = -y
                curr = literals[i]
                aux+=1
            new_clauses.append([prev,curr,literals[-1]])
    return (aux-1),new_clauses

#MAPPING VERIFIER (3-SAT -> SAT)


def verify_projection_preserves_satisfiability(
    original_clauses,
    reduced_clauses,
    assignment_reduced,
    num_original_vars
):
    """
    Verifies that projecting a satisfying assignment of the 3SAT formula
    gives a satisfying assignment of the original SAT formula."""
    

    # Step 1: check assignment satisfies reduced 3SAT formula
    if not verify_sat(reduced_clauses, assignment_reduced):
        raise ValueError("Assignment does NOT satisfy the reduced 3SAT formula")

    # Step 2: project to original variables
    projected = project_assignment(assignment_reduced, num_original_vars)

    # Step 3: check projected assignment satisfies original SAT
    return verify_sat(original_clauses, projected)


def project_assignment(assignment, num_original_vars):
    """
    Keep only assignments for original variables (1..num_original_vars)
    """
    return {
        var: value
        for var, value in assignment.items()
        if 1 <= var <= num_original_vars
    }
