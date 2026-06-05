"""
LeetCode 26. 删除有序数组重复项
题目：给你一个有序数组 nums，请你原地删除重复出现的元素，使每个元素只出现一次，
      返回删除后数组的新长度。不要使用额外的数组空间，必须在原地修改输入数组。

难度：Easy
标签：数组、双指针

解题思路：
- 使用双指针法，一个指针 slow 记录不重复元素的下一个位置，另一个指针 fast 遍历数组
- 当 nums[fast] != nums[slow-1] 时，说明遇到了新的不重复元素
- 将其复制到 slow 位置，然后 slow++
- 最终 slow 的值就是新长度

关键点：
1. 不能用 set 等额外数据结构（题目要求原地修改，空间 O(1)）
2. 只 return slow 一个整数
3. LeetCode 判题时会检查 nums[:slow] 是否为去重后的结果
"""


# ==================== LeetCode 函数模式 ====================
from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        """双指针解法"""
        if not nums:
            return 0

        slow = 1  # slow 指向下一个不重复元素要填入的位置
        for fast in range(1, len(nums)):
            # 如果当前元素和上一个不重复元素不同
            if nums[fast] != nums[slow - 1]:
                nums[slow] = nums[fast]  # 填入不重复元素
                slow += 1                # slow 前移

        return slow  # 只返回这一个整数！


# ==================== ACM 模式（笔试训练） ====================
# 注意：ACM 模式和 LeetCode 模式的区别
# - LeetCode：函数模式，只 return，不写 input/print
# - ACM：自己处理输入输出，用于大厂笔试训练

def remove_duplicates_acm(nums: list[int]) -> int:
    """ACM 模式的双指针解法"""
    if not nums:
        return 0

    slow = 1
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow - 1]:
            nums[slow] = nums[fast]
            slow += 1

    return slow


if __name__ == "__main__":
    # 读取输入
    # 格式：第一行是数组长度，第二行是数组元素（空格分隔）
    # 例如：
    # 10
    # 0 0 1 1 1 2 2 3 3 4
    n = int(input())
    nums = list(map(int, input().split()))

    # 计算结果
    k = remove_duplicates_acm(nums)

    # 输出结果
    # 第一行：新长度
    # 后面若干行：去重后的数组前 k 个元素
    print(k)
    print(' '.join(map(str, nums[:k])))
