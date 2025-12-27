import requests
from typing import List
#dimacs reader/writer for SAT/3-SAT
def dimacs_reader(filepath):
    output=[]
    num_variables = 0
    with open(filepath,"r") as f:
        for line in f:
            line = line.strip()
            if line == "" or line.startswith('c'):
                continue
            elif line.startswith('p'):
                parts = line.split()
                num_variables = int(parts[2])
            else:
                literals = list(map(int,line.split()))
                if literals[-1]==0:
                    literals = literals[:-1]
                output.append(literals)
    return num_variables,output

def write_dimacs(filepath, num_variables, clauses):
    """
    Write clauses to a DIMACS CNF file.
    """
    with open(filepath, "w") as f:
        # Header
        f.write(f"p cnf {num_variables} {len(clauses)}\n")
        
        # Write each clause
        for clause in clauses:
            line = " ".join(str(lit) for lit in clause) + " 0\n"
            f.write(line)

# reader/Writer for SUBSETSUM
BASE_URL = "https://people.sc.fsu.edu/~jburkardt/datasets/subset_sum"

def load_instance(instance: str):
   
    # Download weights
    w_url = f"{BASE_URL}/{instance}_w.txt"
    w_resp = requests.get(w_url)
    w_resp.raise_for_status()
    w_text = w_resp.text.strip()
    # numbers may span multiple lines
    nums: List[int] = []
    for line in w_text.splitlines():
        if line.strip():
            nums.extend(map(int, line.split()))

    # Download target
    c_url = f"{BASE_URL}/{instance}_c.txt"
    c_resp = requests.get(c_url)
    c_resp.raise_for_status()
    target = int(c_resp.text.strip())

    # Download known 0/1 solutions
    s_url = f"{BASE_URL}/{instance}_s.txt"
    s_resp = requests.get(s_url)
    s_resp.raise_for_status()
    known_solutions_01 = [
        line.strip() for line in s_resp.text.splitlines() if line.strip()
    ]

    return nums, target, known_solutions_01


def write_subsetsum_instance(prefix, weights, target, solutions=None):
    """
    Writes a SUBSETSUM instance in the format:
      prefix_c.txt : target
      prefix_w.txt : weights
      prefix_s.txt : solutions (vertical binary format)
    """

    # write target
    with open(f"reduced_subsetsum/{prefix}_c.txt", "w") as f:
        f.write(str(target) + "\n")

    # write weights
    with open(f"reduced_subsetsum/{prefix}_w.txt", "w") as f:
        for w in weights:
            f.write(str(w) + "\n")

    # write solutions (VERTICAL format)
    if solutions is not None:
        num_weights = len(weights)
        num_solutions = len(solutions)

        with open(f"reduced_subsetsum/{prefix}_s.txt", "w") as f:
            for i in range(num_weights):        # for each weight
                row = []
                for k in range(num_solutions):  # for each solution
                    row.append(str(solutions[k][i]))
                f.write("  ".join(row) + "\n")



