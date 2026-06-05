"""
0322. 零钱兑换 / Coin Change

题目：给你一个整数数组 coins，表示不同面额的硬币；以及一个整数 amount，表示总金额。
      计算并返回可以凑成总金额所需的最少的硬币个数。如果没有任何一种硬币组合能组成总金额，返回 -1。
      你可以认为每种硬币的数量是无限的。

输入：
  第一行：硬币面额数组（空格分隔）
  第二行：目标金额

示例：
  1 2 5
  11
  输出: 3
"""

class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        """
        完全背包问题：求最少硬币数

        dp[i] = 组成金额 i 所需的最少硬币个数

        时间复杂度: O(amount * len(coins))
        空间复杂度: O(amount)
        """
        # 初始化：dp[i] 先设为不可能的大值（大于最大可能答案）
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0  # 金额0不需要任何硬币

        # 遍历所有金额
        for i in range(1, amount + 1):
            # 遍历每个硬币面额
            for coin in coins:
                if i >= coin:
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        # 如果无法凑成，返回 -1
        return -1 if dp[amount] > amount else dp[amount]


# ================ ACM模式 ================
if __name__ == "__main__":
    # 第一行：硬币面额数组
    coins = list(map(int, input().split()))
    # 第二行：目标金额
    amount = int(input())

    sol = Solution()
    print(sol.coinChange(coins, amount))