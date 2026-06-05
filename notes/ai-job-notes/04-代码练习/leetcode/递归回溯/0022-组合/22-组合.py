from typing import List

class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        result = []

        def backtrack(start, path):
            if len(path) == k:
                result.append(path.copy())
                return

            for i in range(start, n + 1):
                # 剪枝：剩余元素不够
                if len(path) + (n - i + 1) < k:
                    break
                path.append(i)
                backtrack(i + 1, path)
                path.pop()

        backtrack(1, [])
        return result
