# 19. 反转链表
# https://leetcode.cn/problems/reverse-linked-list/
# 难度：Easy
# 题型：链表

"""
==========================================
📜 题目描述
==========================================
给你单链表的头节点 head，反转链表，返回反转后的头节点。

示例 1：
    输入：head = [1,2,3,4,5]
    输出：[5,4,3,2,1]

示例 2：
    输入：head = [1,2]
    输出：[2,1]

==========================================
💡 解题思路
==========================================
双指针迭代（推荐）：
- prev = None, curr = head
- 每次反转 curr.next，然后移动 prev 和 curr
- 最终 prev 就是新头节点

时间复杂度：O(n)
空间复杂度：O(1)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        prev = None
        curr = head

        while curr:
            next_temp = curr.next  # 保存下一个节点
            curr.next = prev       # 反转指针
            prev = curr            # prev 移动
            curr = next_temp       # curr 移动

        return prev


if __name__ == "__main__":
    pass
