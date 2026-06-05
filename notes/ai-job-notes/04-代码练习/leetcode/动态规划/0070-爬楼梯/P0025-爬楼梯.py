"""
P0025-爬楼梯
动态规划入门：斐波那契数列

题目：假设你正在爬楼梯，需要n阶才能到达楼顶。每次你可以爬1或2个台阶。
      求有多少种不同的方法可以爬到楼顶。

输入：n - 楼梯阶数
输出：爬到楼顶的不同方法数

示例：
输入: 2
输出: 2
"""

class Solution:
    def climbStairs(self, n: int) -> int:
        """
        动态规划解法：
        dp[i] 表示爬到第i阶楼梯的方法数
        dp[1] = 1
        dp[2] = 2
        dp[i] = dp[i-1] + dp[i-2]  (i >= 3)
        """
        if n <= 2:
            return n

        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2

        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]


# ================ ACM模式 ================
if __name__ == "__main__":
    n = int(input().strip())

    sol = Solution()
    print(sol.climbStairs(n))