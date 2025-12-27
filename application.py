from read_write_files import *
from sat_sat3 import *
from sat_subsetsum import *
from subsetsum import *
from sat import solve_sat_bruteforce
def main():
    print("==== SAT Tools ====")
    print("1: SAT Solver and verifier")
    print("2: SUBSETSUM Solver and verifier")
    print("3: SAT -> 3SAT reduction")
    print("4: SAT -> SubsetSum reduction")
    choice = input("Choose option : ").strip()

    if choice == "1":
        variables, clauses = 5, [[1,2,4,-7],[2,-3],[-4,-5]]
        solution = solve_sat_bruteforce(clauses,variables)
        if solution is False:
            print("UNSAT")
        else :
            print(f"solution : {solution}")
            print("verifier : ")
            s = verify_sat(clauses,solution)
            if s:
                print("solution correct")
            else :
                print("solution incorrect") 
    elif choice == "2":
        instance_name = "p06"
        nums, target, known_solutions_01 = load_instance(instance_name)
        print(f"Instance: {instance_name}")
        print(f"Numbers ({len(nums)}): {nums}")
        print(f"Target: {target}")
        solutions = subsets(nums, target)
        print(f"\nTotal backtracking solutions found: {len(solutions)}")
        print("\nBacktracking solutions in 0/1 format:")
        for subset in solutions:
            binary = subset_to_binary(nums, subset)
            print(binary)
        dp_solution = dp_subset_sum_one(nums, target)
        if dp_solution:
            print("\nDP found one solution (values):", dp_solution)
            print("DP solution in 0/1 format:", subset_to_binary(nums, dp_solution))
        else:
            print("\nDP found no solution.")
       
    elif choice == "3":
        original_variables, original_clauses = 5, [[1],[2,-3],[-4,-5]]
        new_variables, new_clauses = sat_3sat(original_clauses, original_variables+1)
        write_dimacs("reduced_3sat/new.cnf", new_variables, new_clauses)

        print("3-SAT clauses (first 10):")
        for c in new_clauses[:10]:
            print(c)

        print(f"Original variables: {original_variables}, Total variables after reduction: {new_variables}")
        print(f"Original clauses: {len(original_clauses)}, Total clauses after reduction: {len(new_clauses)}")
        solution = solve_sat_bruteforce(new_clauses,new_variables)
        ver = verify_projection_preserves_satisfiability(original_clauses,new_clauses,solution,original_variables)
        if ver:
            print("SAT preserved")
        else:
            print("SAT unpreserved")

    elif choice == "4":
        clauses = [[1,3],[1,-2],[2,3,4,5]]
        num_vars = 5
        numbers, target, meta = sat_to_subsetsum_base2(clauses, num_vars)

        # Example satisfying assignment
        assignment = {1: False, 2: False, 3: True, 4: False, 5: False}
        subset = sat_solution_to_subset(assignment, numbers, meta, clauses)
        binary_solution = subset_to_binary_solution(subset, numbers)

        write_subsetsum_instance(
            prefix="p09",
            weights=numbers,
            target=target,
            solutions=[binary_solution]
        )

        print("SubsetSum numbers:")
        for n in numbers:
            print(n)
        print("Subset sum:", sum(subset))
        print("Target:    ", target)
        print("Equal?     ", sum(subset) == target)
    
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()