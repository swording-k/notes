# 10. 存在重复元素
# https://leetcode.cn/problems/contains-duplicate/
# 难度：Easy
# 题型：哈希表

"""
==========================================
📜 题目描述
==========================================
给你一个整数数组 nums。如果任一值在数组中出现至少两次，返回 true；否则返回 false。

示例 1：
    输入：nums = [1,2,3,1]
    输出：true
    解释：元素 1 出现了两次

示例 2：
    输入：nums = [1,2,3,4]
    输出：false
    解释：所有元素都不重复

示例 3：
    输入：nums = [1,1,1,3,3,4,3,2,4,2]
    输出：true
    解释：有多个重复元素

==========================================
💡 解题思路
==========================================

【方法1】字典计数法（你的写法，已修复）
时间复杂度：O(n)，空间复杂度：O(n)

【方法2】set 去重法（更简洁，推荐）
时间复杂度：O(n)，空间复杂度：O(n)
"""

# 方法1：字典计数法（你的修复版本）
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        count = {}
        for i in range(0, len(nums)):
            if nums[i] in count:
                count[nums[i]] += 1
            else:
                count[nums[i]] = 1
            if count[nums[i]] >= 2:
                return True
        return False


# 方法2：set 去重法（推荐）
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False


# ===== ACM 模式输入输出 =====
if __name__ == "__main__":
    import sys

    # 读取一行输入，转换为整数列表
    line = sys.stdin.readline().strip()
    nums = list(map(int, line.split()))

    # 输出结果
    solution = Solution()
    result = solution.containsDuplicate(nums)
    print("true" if result else "false")
