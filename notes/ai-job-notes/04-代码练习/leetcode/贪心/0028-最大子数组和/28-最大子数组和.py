from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = nums[0]    # 全局最大和
        cur_sum = nums[0]   # 当前连续和

        for i in range(1, len(nums)):
            # 贪心：重新开始 vs 继续累加
            cur_sum = max(nums[i], cur_sum + nums[i])
            max_sum = max(max_sum, cur_sum)

        return max_sum