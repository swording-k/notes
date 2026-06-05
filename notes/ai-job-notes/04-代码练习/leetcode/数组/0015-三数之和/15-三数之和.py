from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()           # 1. 先排序
        result = []

        for k in range(len(nums) - 2):  # k 是固定的第三个数字
            if nums[k] > 0:             # 最小的都大于0，不可能有0
                break
            if k > 0 and nums[k] == nums[k-1]:  # 去重，跳过相同元素
                continue

            i, j = k + 1, len(nums) - 1  # 双指针

            while i < j:
                s = nums[k] + nums[i] + nums[j]
                if s < 0:
                    i += 1              # 和太小，增大 i
                elif s > 0:
                    j -= 1              # 和太大，减小 j
                else:
                    result.append([nums[k], nums[i], nums[j]])
                    i += 1
                    j -= 1
                    while i < j and nums[i] == nums[i-1]:
                        i += 1          # 跳过重复的 i
                    while i < j and nums[j] == nums[j+1]:
                        j -= 1          # 跳过重复的 j

        return result