"""
0279. 完全平方数 / Perfect Squares

题目：给你一个整数 n，返回和为 n 的完全平方数的最少数量。
      完全平方数是一个整数，其值等于另一个整数的平方。

输入: n (1 <= n <= 10^4)
输出: 最少完全平方数数量

示例：
输入: 12
输出: 3
说明: 12 = 4 + 4 + 4
"""

class Solution:
    def numSquares(self, n: int) -> int:
        """
        动态规划解法：
        dp[i] 表示和为 i 的最少完全平方数个数

        转移方程：dp[i] = min(dp[i - j²] + 1) for all j where j² <= i

        时间复杂度：O(n√n)
        空间复杂度：O(n)
        """
        # dp[i] 初始化为正无穷，dp[0] = 0
        dp = [float('inf')] * (n + 1)
        dp[0] = 0

        # 遍历每个数字 i
        for i in range(1, n + 1):
            j = 1
            # 枚举所有可能的完全平方数 j²
            while j * j <= i:
                dp[i] = min(dp[i], dp[i - j * j] + 1)
                j += 1

        return dp[n]


# ================ ACM模式 ================
if __name__ == "__main__":
    n = int(input())
    sol = Solution()
    print(sol.numSquares(n))