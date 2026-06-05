"""
0198. 打家劫舍 / House Robber

题目：你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，
      相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被闯入，
      系统会自动报警。给定一个代表每个房屋存放金额的非负整数数组，
      计算不触动警报装置的情况下，一夜之内能够偷窃到的最高金额。

输入: 一行整数数组，如 "1 2 3 1"
输出: 最大偷窃金额，如 4
"""

class Solution:
    def rob(self, nums: list[int]) -> int:
        """
        动态规划解法：
        dp[i] 表示偷到第 i 个房屋时的最高金额

        转移方程：dp[i] = max(dp[i-1], dp[i-2] + nums[i])
        - 不选当前房屋：dp[i-1]
        - 选当前房屋：dp[i-2] + nums[i]

        时间复杂度：O(n)
        空间复杂度：O(n) → 可优化为 O(1)
        """
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]

        # 初始化
        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])

        # 状态转移
        for i in range(2, n):
            dp[i] = max(dp[i-1], dp[i-2] + nums[i])

        return dp[-1]


# ================ ACM模式 ================
if __name__ == "__main__":
    import sys
    nums = list(map(int, sys.stdin.read().split()))
    solution = Solution()
    print(solution.rob(nums))