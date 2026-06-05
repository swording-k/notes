from typing import List

class Solution:
    def wiggleMaxLength(self, nums: List[int]) -> int:
        if len(nums) < 2:
            return len(nums)

        up = down = 1  # 以上升/下降结尾的最长摆动长度

        for i in range(1, len(nums)):
            if nums[i] > nums[i-1]:
                up = down + 1    # 上升段 = 之前下降段 + 1
            elif nums[i] < nums[i-1]:
                down = up + 1    # 下降段 = 之前上升段 + 1

        return max(up, down)