import sys

class Solution:
    def function(self, m, n, v, swap, rep):
        # 开大一点的数组：最大可能空间 = m + max(单个张量空间)
        max_space = m + max(v)
        dp = [float('inf')] * (max_space + 1)
        dp[0] = 0

        # 0-1背包：每个张量只能选一次
        for i in range(n):
            cost = min(swap[i], rep[i])  # 选 swap 或 recompute，代价小的
            weight = v[i]                # 这个张量占用的空间

            # 从大到小遍历（关键！避免同一个张量被选多次）
            for j in range(max_space, weight - 1, -1):
                if dp[j - weight] != float('inf'):
                    dp[j] = min(dp[j], dp[j - weight] + cost)

        # 找空间 >= m 的最小代价
        result = min(dp[m:])  # dp[m], dp[m+1], ..., dp[max_space] 中找最小
        if result == float('inf'):
            return "error"
        return result


if __name__ == "__main__":
    data = sys.stdin.read().strip().split()
    m = int(data[0])
    n = int(data[1])

    v = list(map(int, data[2:2+n]))
    swap = list(map(int, data[2+n:2+2*n]))
    rep = list(map(int, data[2+2*n:2+3*n]))

    sol = Solution()
    print(sol.function(m, n, v, swap, rep))