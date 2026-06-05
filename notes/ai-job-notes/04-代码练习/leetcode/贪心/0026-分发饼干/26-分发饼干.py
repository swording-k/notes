from typing import List

class Solution:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        g.sort()  # 孩子胃口排序
        s.sort()  # 饼干尺寸排序

        child = 0  # 已满足的孩子数（也是下一个孩子的索引）

        for size in s:  # 遍历每个饼干
            if child < len(g) and size >= g[child]:
                child += 1  # 这个饼干满足了这个孩子

        return child