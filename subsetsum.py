from typing import List

#subset solver
def subsets( nums: List[int], target: int) -> List[List[int]]:
        res = []

        def backtrack(index: int, current_sum: int, current_subset: List[int]):
            if current_sum == target:
                res.append(current_subset[:])
                return

            if current_sum > target or index == len(nums):
                return

            current_subset.append(nums[index])
            backtrack(index + 1, current_sum + nums[index], current_subset)

            current_subset.pop()
            backtrack(index + 1, current_sum, current_subset)

        backtrack(0, 0, [])
        return res


#subset dp solver
def dp_subset_sum_one(nums: List[int], target: int) -> List[int]:
        """
        Bottom-up DP that returns one subset (values) summing to target, or [] if none.
        Assumes non-negative targets.
        """
        n = len(nums)
        if target < 0:
            return []

        dp = [[False] * (target + 1) for _ in range(n + 1)]
        dp[0][0] = True

        for i in range(1, n + 1):
            val = nums[i - 1]
            for s in range(target + 1):
                dp[i][s] = dp[i - 1][s] or (s >= val and dp[i - 1][s - val])

        if not dp[n][target]:
            return []

        subset: List[int] = []
        i, s = n, target
        while i > 0 and s >= 0:
            val = nums[i - 1]
            if s >= val and dp[i - 1][s - val]:
                subset.append(val)
                s -= val
            i -= 1
        subset.reverse()
        return subset
#subset verifier
def subset_to_binary(nums, subset):
    subset_set = set(subset)
    return [1 if num in subset_set else 0 for num in nums]


def verify_against_known_solutions(nums: List[int], target: int,
                                   solutions: List[List[int]],
                                   known_solutions_01: List[str]) -> bool:
    
    ok = True

    # 1) Check each found subset sums to target
    for i, subset in enumerate(solutions):
        s = sum(subset)
        if s != target:
            print(f"[ERROR] Solution #{i} has wrong sum: {subset} (sum={s}, target={target})")
            ok = False

    # 2) Convert backtracking solutions to 0/1 strings
    found_01 = []
    for subset in solutions:
        bits = subset_to_binary(nums, subset)
        found_01.append("".join(str(b) for b in bits))
