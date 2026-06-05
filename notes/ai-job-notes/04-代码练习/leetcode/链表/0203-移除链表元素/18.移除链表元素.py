# 18. 移除链表元素
# https://leetcode.cn/problems/remove-linked-list-elements/
# 难度：Easy
# 题型：链表

"""
==========================================
📜 题目描述
==========================================
给你一个链表的头节点 head 和一个整数 val，删除链表中所有满足
node.val == val 的节点，并返回新的头节点。

示例 1：
    输入：head = [4,2,1,4], val = 4
    输出：[2,1]

示例 2：
    输入：head = [1,2,6,3,4,5,6], val = 6
    输出：[1,2,3,4,5]

==========================================
💡 解题思路
==========================================
两种方法：
1. 虚拟头节点（推荐）：避免处理头节点的特殊情况
2. 直接遍历：需要单独处理头节点

时间复杂度：O(n)
空间复杂度：O(1)
"""

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeElements(self, head: ListNode, val: int) -> ListNode:
        # 虚拟头节点，简化操作
        dummy = ListNode(0, head)
        curr = dummy

        while curr.next:
            if curr.next.val == val:
                curr.next = curr.next.next
            else:
                curr = curr.next

        return dummy.next


if __name__ == "__main__":
    # ACM 模式需要自己解析链表
    # 这里只提供函数模式
    pass
