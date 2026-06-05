"""
0139. 单词拆分 / Word Break

题目：给你一个字符串 s 和一个字符串列表 wordDict 作为字典。
      如果可以利用字典中出现的一个或多个单词拼接出 s 则返回 true。
      不要求字典中出现的单词全部都使用，并且字典中的单词可以重复使用。

输入：
  第一行：字符串 s
  第二行：字典单词列表（空格分隔）

示例：
  leetcode
  leet code
  输出: true
"""

class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        """
        动态规划解法

        dp[i] 表示 s[0:i] 是否可以被切分成字典中的单词

        时间复杂度: O(n²)
        空间复杂度: O(n)
        """
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True  # 空串可以被成功切分

        # 遍历字符串每个位置
        for i in range(1, n + 1):
            # 枚举所有可能的切分点 j
            for j in range(i):
                # 如果 s[0:j] 可切分 且 s[j:i] 在字典中
                if dp[j] and s[j:i] in wordDict:
                    dp[i] = True
                    break  # 找到一种切分方式即可退出

        return dp[n]


# ================ ACM模式 ================
if __name__ == "__main__":
    # 第一行：字符串 s
    s = input().strip()
    # 第二行：字典单词列表（空格分隔）
    wordDict = set(input().split())

    sol = Solution()
    result = sol.wordBreak(s, wordDict)
    print("true" if result else "false")